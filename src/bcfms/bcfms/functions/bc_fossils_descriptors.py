from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from bcfms.util.bcfms_aliases import (
    GraphSlugs,
    CollectionEventAliases as aliases,
    FossilSampleAliases as sample_aliases,
)
from bcfms.util.scientific_terms_util import ScientificTermsFormatter
from bcgov_arches_common.util.graph_lookup import GraphLookup
from bcgov_arches_common.util.bc_primary_descriptors_function import BCPrimaryDescriptorsFunction

details = {
    "functionid": "60000000-0000-0000-0000-000000001001",
    "name": "BC Fossils Resource Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossils_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Fossils resources",
    "defaultconfig": {
        "module": "bcfms.functions.bc_fossils_descriptors",
        "class_name": "BCFossilsDescriptors",
        "descriptor_types": {
            "name": {
                "type": "name",
                "node_ids": [],
                "first_only": True,
                "show_name": False,
            },
            "description": {
                "type": "description",
                "node_ids": [],
                "first_only": False,
                "delimiter": "<br>",
                "show_name": True,
            },
            "map_popup": {
                "type": "map_popup",
                "node_ids": [],
                "first_only": False,
                "delimiter": "<br>",
                "show_name": True,
            },
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCFossilsDescriptors",
    "component": "views/components/functions/bc-fossils-descriptors",
}


class BCFossilsDescriptors(BCPrimaryDescriptorsFunction):
    _sample_graph_name = {"en": "Fossil Sample"}
    _datatype_factory = None
    _formation_node = None
    _geologic_minimum_time_node = None
    _collected_fossils_node = None
    _collection_event_graph_id = None
    _coll_event_samples_values_config = None
    _coll_event_popup_order = [
        "Detailed Location",
        "Formation",
        "Period",
        "Samples Collected",
    ]
    _coll_event_card_order = ["Detailed Location", "Period", "Samples Collected"]

    _ce_graph_lookup = None
    _fs_graph_lookup = None

    _ce_graph_slug = GraphSlugs.COLLECTION_EVENT
    _fs_graph_slug = GraphSlugs.FOSSIL_SAMPLE

    _ce_name_aliases = [
        aliases.START_YEAR,
        aliases.LOCATION_DESCRIPTOR,
        aliases.NTS_MAPSHEET_NAME,
    ]
    _ce_popup_aliases = [aliases.DETAILED_LOCATION]
    _ce_search_card_aliases = [aliases.DETAILED_LOCATION]

    _ce_sample_aliases = [
        sample_aliases.SCIENTIFIC_NAME,
        sample_aliases.NAME_CONNECTOR,
        sample_aliases.OTHER_SCIENTIFIC_NAME,
        sample_aliases.FOSSIL_COMMON_NAME,
        sample_aliases.COMMON_NAME_UNCERTAIN,
        sample_aliases.GEOLOGICAL_FORMATION,
        sample_aliases.GEOLOGICAL_FORMATION_UNCERTAIN,
        sample_aliases.MINIMUM_TIME,
        sample_aliases.MINIMUM_TIME_UNCERTAIN,
    ]

    def __init__(self):
        super(BCFossilsDescriptors).__init__()
        self._ce_graph_lookup = GraphLookup(
            BCFossilsDescriptors._ce_graph_slug,
            list(
                set(
                    BCFossilsDescriptors._ce_name_aliases
                    + BCFossilsDescriptors._ce_popup_aliases
                    + BCFossilsDescriptors._ce_search_card_aliases
                )
            ),
        )
        self._fs_graph_lookup = GraphLookup(
            BCFossilsDescriptors._fs_graph_slug, BCFossilsDescriptors._ce_sample_aliases
        )

    @staticmethod
    def initialize_static_data():
        BCFossilsDescriptors._formation_node = models.Node.objects.filter(
            alias="geological_formation",
            graph__name__contains=BCFossilsDescriptors._sample_graph_name,
        ).first()
        BCFossilsDescriptors._geologic_minimum_time_node = models.Node.objects.filter(
            alias="minimum_time",
            graph__name__contains=BCFossilsDescriptors._sample_graph_name,
        ).first()
        BCFossilsDescriptors._collected_fossils_node = models.Node.objects.filter(
            alias="samples_collected",
        ).first()
        BCFossilsDescriptors._collection_event_graph_id = (
            models.GraphModel.objects.filter(
                name__contains={"en": "Fossil Collection Event"}
            )
            .filter(isresource=True)
            .values("graphid")
            .first()["graphid"]
        )
        BCFossilsDescriptors._coll_event_samples_values_config = [
            {"node": BCFossilsDescriptors._formation_node, "label": "Formation"},
            {
                "node": BCFossilsDescriptors._geologic_minimum_time_node,
                "label": "Period",
            },
        ]

    def get_primary_descriptor_from_nodes(
        self, resource, config, context=None, descriptor=None
    ):
        return_value = ""
        display_values = {}

        if BCFossilsDescriptors._formation_node is None:
            BCFossilsDescriptors.initialize_static_data()

        try:
            if resource.graph_id == self._collection_event_graph_id:
                if descriptor == "name":
                    return self._get_site_name(resource)
                else:
                    return_value = self.format_value(
                        "Detailed Location",
                        self.get_value_from_node(
                            self._ce_graph_lookup.get_node(aliases.DETAILED_LOCATION),
                            self._ce_graph_lookup.get_datatype(
                                aliases.DETAILED_LOCATION
                            ),
                            resourceinstanceid=resource.resourceinstanceid,
                        ),
                    )
                    samples = self._get_samples(resource)
                    if descriptor == "map_popup":
                        return_value += self._get_values_from_samples(
                            samples,
                            "Formation",
                            sample_aliases.GEOLOGICAL_FORMATION,
                            sample_aliases.GEOLOGICAL_FORMATION_UNCERTAIN,
                        )

                    return_value += self._get_values_from_samples(
                        samples,
                        "Period",
                        sample_aliases.MINIMUM_TIME,
                        sample_aliases.MINIMUM_TIME_UNCERTAIN,
                    )

                    if descriptor == "description":
                        scientific_names = self.get_scientific_names_from_samples(
                            samples
                        )
                        return_value += (
                            scientific_names
                            if scientific_names != ""
                            else self.get_common_names_from_samples(samples)
                        )

                return return_value

            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                nodeid__in=config["node_ids"]
            )
            sorted_name_nodes = sorted(
                name_nodes,
                key=lambda row: config["node_ids"].index(str(row.nodeid)),
                reverse=False,
            )

            for name_node in sorted_name_nodes:
                # print("Name node: %s" % name_node.alias)
                value = self._get_value_from_node(name_node, resource)
                if value:
                    if config["first_only"]:
                        return self.format_value(
                            name_node.name, value, config["show_name"]
                        )
                    display_values[name_node.name] = value

            # if resource.graph_id == BCFossilsDescriptors._collection_event_graph_id:
            #     for label in (
            #             BCFossilsDescriptors._coll_event_popup_order if config["type"] == "map_popup" else BCFossilsDescriptors._coll_event_card_order):
            #         if label in display_values:
            #             if not return_value:
            #                 return_value = ""
            #             else:
            #                 return_value += config["delimiter"]
            #             return_value += self.format_value(label, display_values[label], config)
            # else:
            for key in display_values.keys():
                if not return_value:
                    return_value = ""
                else:
                    return_value += config["delimiter"]
                return_value += self.format_value(
                    key, display_values[key], config["show_name"]
                )

            return return_value
        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_value_from_node(self, name_node, resourceinstanceid):

        tile = (
            models.TileModel.objects.filter(nodegroup_id=name_node.nodegroup_id)
            .filter(resourceinstance_id=resourceinstanceid)
            .first()
        )
        if not tile:
            return None
        datatype = self._get_datatype_factory().get_instance(name_node.datatype)
        return datatype.get_display_value(tile, name_node)

    def _get_datatype_factory(self):
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
        return self._datatype_factory

    def _get_samples(self, resource):
        return models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=resource.resourceinstanceid,
            nodeid=BCFossilsDescriptors._collected_fossils_node.nodeid,
        ).values_list("resourceinstanceidto", flat=True)

    def get_scientific_names_from_samples(self, samples, formatted=True):
        values = []
        # sample_ids = list(map(lambda sample: sample.resourceinstanceid, samples))
        sample_ids = samples
        tiles = models.TileModel.objects.filter(
            nodegroup_id=self._fs_graph_lookup.get_node(
                sample_aliases.SCIENTIFIC_NAME
            ).nodegroup_id,
            resourceinstance_id__in=sample_ids,
        ).all()
        for tile in tiles:
            values.append(
                ScientificTermsFormatter.format_scientific_name(
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(sample_aliases.SCIENTIFIC_NAME),
                        self._fs_graph_lookup.get_datatype(
                            sample_aliases.SCIENTIFIC_NAME
                        ),
                        data_tile=tile,
                    ),
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(sample_aliases.NAME_CONNECTOR),
                        self._fs_graph_lookup.get_datatype(
                            sample_aliases.NAME_CONNECTOR
                        ),
                        data_tile=tile,
                    ),
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(
                            sample_aliases.OTHER_SCIENTIFIC_NAME
                        ),
                        self._fs_graph_lookup.get_datatype(
                            sample_aliases.OTHER_SCIENTIFIC_NAME
                        ),
                        data_tile=tile,
                    ),
                )
            )
            values = list(filter(lambda val: val is not None, values))
            values.sort()
        return (
            self.format_value("Scientific Names", values, value_connector="<br>")
            if formatted
            else values
        )

    def get_common_names_from_samples(self, samples, formatted=True):
        values = []
        sample_ids = samples
        tiles = models.TileModel.objects.filter(
            nodegroup_id=self._fs_graph_lookup.get_node(
                sample_aliases.SCIENTIFIC_NAME
            ).nodegroup_id,
            resourceinstance_id__in=sample_ids,
        ).all()
        for tile in tiles:
            values.append(
                ScientificTermsFormatter.format_uncertain(
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(
                            sample_aliases.FOSSIL_COMMON_NAME
                        ),
                        self._fs_graph_lookup.get_datatype(
                            sample_aliases.FOSSIL_COMMON_NAME
                        ),
                        data_tile=tile,
                    ),
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(
                            sample_aliases.COMMON_NAME_UNCERTAIN
                        ),
                        self._fs_graph_lookup.get_datatype(
                            sample_aliases.COMMON_NAME_UNCERTAIN
                        ),
                        data_tile=tile,
                    ),
                )
            )
        return self.format_value("Common Names", values)

    def _get_values_from_samples(
        self, samples, label, node_alias, uncertainty_alias=None
    ):
        values = []
        for sample in samples:
            if uncertainty_alias is None:
                values.append(
                    self.get_value_from_node(
                        self._fs_graph_lookup.get_node(node_alias),
                        self._fs_graph_lookup.get_datatype(node_alias),
                        resourceinstanceid=sample,
                    )
                )
            else:
                values.append(
                    ScientificTermsFormatter.format_uncertain(
                        self.get_value_from_node(
                            self._fs_graph_lookup.get_node(node_alias),
                            self._fs_graph_lookup.get_datatype(node_alias),
                            resourceinstanceid=sample,
                        ),
                        self.get_value_from_node(
                            self._fs_graph_lookup.get_node(uncertainty_alias),
                            self._fs_graph_lookup.get_datatype(uncertainty_alias),
                            resourceinstanceid=sample,
                            use_boolean_label=False,
                        ),
                    )
                )
        # values = [val for val in values if val is not None and val != ""]
        # print("Node alias: %s values: %s" % (node_alias, values))
        # return "" if len(values) == 0 else self.format_value(label, values)
        # print("Returning: %s" % self.format_value(label, values))
        return self.format_value(label, values)

    def _get_sample_values(self, resource, values_config):
        # print("Resource: %s" % resource.resourceinstanceid)
        return_values = {}

        fossil_sample_values = models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=resource.resourceinstanceid,
            nodeid=BCFossilsDescriptors._collected_fossils_node.nodeid,
        ).values_list("resourceinstanceidto", flat=True)

        for child_values in values_config:
            tiles = models.TileModel.objects.filter(
                nodegroup_id=child_values["node"].nodegroup_id,
                resourceinstance_id__in=fossil_sample_values,
            ).all()

            if len(tiles) != 0:
                datatype = self._get_datatype_factory().get_instance(
                    child_values["node"].datatype
                )

                values = []
                for tile in tiles:
                    period_value = datatype.get_display_value(
                        tile, child_values["node"]
                    )
                    if period_value:
                        values.append(period_value)

                if len(values) > 0:
                    return_values[child_values["label"]] = ", ".join(list(set(values)))
        return return_values

    def _get_site_name(self, resource):
        start_year = self.get_value_from_node(
            self._ce_graph_lookup.get_node(aliases.START_YEAR),
            self._ce_graph_lookup.get_datatype(aliases.START_YEAR),
            resourceinstanceid=resource.resourceinstanceid,
        )

        location_descriptor = self.get_value_from_node(
            self._ce_graph_lookup.get_node(aliases.LOCATION_DESCRIPTOR),
            self._ce_graph_lookup.get_datatype(aliases.LOCATION_DESCRIPTOR),
            resourceinstanceid=resource.resourceinstanceid,
        )

        if not location_descriptor:
            location_descriptor = self.get_value_from_node(
                self._ce_graph_lookup.get_node(aliases.NTS_MAPSHEET_NAME),
                self._ce_graph_lookup.get_datatype(aliases.NTS_MAPSHEET_NAME),
                resourceinstanceid=resource.resourceinstanceid,
            )

        return "(%s) - %s" % (
            "?" if not start_year else start_year,
            "Unknown" if not location_descriptor else location_descriptor,
        )
