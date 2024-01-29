from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
import re
from bcfms.util.scientific_terms_util import ScientificTermsFormatter as NameFormatter

details = {
    "functionid": "60000000-0000-0000-0000-000000001004",
    "name": "BC Fossil Samples Resource Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossil_sample_descriptors.py",
    "description": "Function that provides the primary descriptors for Fossil Sample resources",
    "defaultconfig": {
        "module": "bcfms.functions.bc_fossil_sample_descriptors",
        "class_name": "BCFossilSampleDescriptors",
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
    "classname": "BCFossilSampleDescriptors",
    "component": "views/components/functions/bc-fossil-sample-descriptors",
}


class BCFossilSampleDescriptors(AbstractPrimaryDescriptorsFunction):
    _sample_graph_slug = "fossil_sample"
    _datatype_factory = None
    _sample_name_nodes = ["storage_reference", "field_number"]
    _sample_card_order = ["scientific_name", "open_nomanclature_term", "other_scientific_name",
                          "fossil_common_name","common_name_uncertain",
                          "fossil_size_category_v",
                          "minimum_time", "minimum_time_uncertain", "maximum_time","maximum_time_uncertain",
                          "geological_group", "geological_group_uncertain",
                          "geological_formation", "geological_formation_uncertain",
                          "geological_member", "geological_member_uncertain",
                          "informal_map_unit_or_name", "other_stratigraphic_name"
                          ]
    _nodes = {}
    # _titles = {"scientific_name": "",
    #            "open_nomanclature_term"
    #             "other_scientific_name", "fossil_size_category_v", "minimum_time", "minimum_time_uncertain", "maximum_time","maximum_time_uncertain"}

    @staticmethod
    def initialize_static_data():
        print("Initializing nodes...")
        for alias in BCFossilSampleDescriptors._sample_name_nodes + BCFossilSampleDescriptors._sample_card_order:
            BCFossilSampleDescriptors._nodes[alias] = models.Node.objects.filter(
                alias=alias,
                graph__slug=BCFossilSampleDescriptors._sample_graph_slug
            ).first()

    def get_primary_descriptor_from_nodes(self, resource, config, context=None, descriptor=None):
        return_value = None
        display_values = []

        if len(BCFossilSampleDescriptors._nodes) == 0:
            BCFossilSampleDescriptors.initialize_static_data()

        try:
            if config["type"] == "name":
                return self._get_site_name(resource)

            return "<dl>%s</dl>" % (self._get_scientific_names(resource)
                +self._get_common_names(resource)
                +self._format_value("Size Category", self._get_value_from_node(self._nodes["fossil_size_category_v"], resource))
                +self._get_sample_ages(resource)
                +self._get_stratigraphy(resource))

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")


    def _get_scientific_names(self, resourceinstanceid):
        tiles = models.TileModel.objects.filter(
            nodegroup_id=BCFossilSampleDescriptors._nodes["scientific_name"].nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).all()
        scientific_names = []
    # _sample_card_order = ["scientific_name", "open_nomanclature_term", "other_scientific_name", "fossil_size_category_v", "minimum_time", "minimum_time_uncertain", "maximum_time","maximum_time_uncertain"]
        sci_name_node = BCFossilSampleDescriptors._nodes["scientific_name"]
        sci_name_dt = self._get_datatype_factory().get_instance(sci_name_node.datatype)
        open_nom_node = BCFossilSampleDescriptors._nodes["open_nomanclature_term"]
        open_nom_dt = self._get_datatype_factory().get_instance(open_nom_node.datatype)
        other_sci_name_node = BCFossilSampleDescriptors._nodes["other_scientific_name"]
        other_sci_name_dt = self._get_datatype_factory().get_instance(other_sci_name_node.datatype)

        for tile in tiles:
            scientific_names.append(NameFormatter.format_scientific_name(
                sci_name_dt.get_display_value(tile, sci_name_node),
                open_nom_dt.get_display_value(tile, open_nom_node),
                other_sci_name_dt.get_display_value(tile, other_sci_name_node)
            ))
        scientific_names = [x for x in scientific_names if x is not None]

        return "" if len(scientific_names) == 0 else "<dt>Scientific Names</dt><dd>%s</dd>"% "<br>".join(scientific_names)

    def _get_common_names(self, resourceinstanceid):
        tiles = models.TileModel.objects.filter(
            nodegroup_id=BCFossilSampleDescriptors._nodes["fossil_common_name"].nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).all()

        common_names = []
        common_name_node = BCFossilSampleDescriptors._nodes["fossil_common_name"]
        common_name_dt = self._get_datatype_factory().get_instance(common_name_node.datatype)
        common_name_uncertain_node = BCFossilSampleDescriptors._nodes["common_name_uncertain"]
        # common_name_uncertain_dt = self._get_datatype_factory().get_instance(common_name_node.datatype)

        for tile in tiles:
            common_names.append(NameFormatter.format_common_name(
                common_name_dt.get_display_value(tile, common_name_node),
                tile.data[str(common_name_uncertain_node.nodeid)]
            ))
        common_names = [x for x in common_names if x is not None]

        return "" if len(common_names) == 0 else "<dt>Common Names</dt><dd>%s</dd>"% "<br>".join(common_names)

    def _get_sample_ages(self, resourceinstanceid):
        tile = models.TileModel.objects.filter(
            nodegroup_id=BCFossilSampleDescriptors._nodes["minimum_time"].nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()

        if not tile:
            return ""

        min_time_node = BCFossilSampleDescriptors._nodes["minimum_time"]
        min_time_dt = self._get_datatype_factory().get_instance(min_time_node.datatype)
        min_time_uncertain_node = BCFossilSampleDescriptors._nodes["minimum_time_uncertain"]

        max_time_node = BCFossilSampleDescriptors._nodes["maximum_time"]
        max_time_dt = self._get_datatype_factory().get_instance(max_time_node.datatype)
        max_time_uncertain_node = BCFossilSampleDescriptors._nodes["maximum_time_uncertain"]

        return self._format_value("Geological Age", NameFormatter.format_times(
            min_time_dt.get_display_value(tile, min_time_node),
            tile.data[str(min_time_uncertain_node.nodeid)],
            max_time_dt.get_display_value(tile, max_time_node),
            tile.data[str(max_time_uncertain_node.nodeid)]
        ))

    def _get_stratigraphy(self, resourceinstanceid):
        return_value = ""
        tile = models.TileModel.objects.filter(
            nodegroup_id=BCFossilSampleDescriptors._nodes["geological_group"].nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()

        formal_nodes = [
            {"title": "Geological Group", "node_name": "geological_group",
             "uncertain_node_name": "geological_group_uncertain"},
            {"title": "Geological Formation", "node_name": "geological_formation",
             "uncertain_node_name": "geological_formation_uncertain"},
            {"title": "Geological Member", "node_name": "geological_member",
             "uncertain_node_name": "geological_member_uncertain"},
                             ]

        informal_nodes = [
            {"title": "Informal Map Unit or Name", "node_name": "informal_map_unit_or_name"},
            {"title": "Other Stratigraphic Name", "node_name": "other_stratigraphic_name"}
        ]

        if not tile:
            return return_value
        else:
            for node_config in formal_nodes:
                node = BCFossilSampleDescriptors._nodes[node_config["node_name"]]
                value = self._get_datatype_factory().get_instance(node.datatype).get_display_value(tile, node)
                if value:
                    value = NameFormatter.format_uncertain(value, tile.data[str(BCFossilSampleDescriptors._nodes[node_config["uncertain_node_name"]].nodeid)])
                    if value:
                        return_value += self._format_value(node_config["title"], value)
            # Didn't find a formal name so try informal ones
            if not return_value:
                for node_config in informal_nodes:
                    node = BCFossilSampleDescriptors._nodes[node_config["node_name"]]
                    return_value += self._format_value(node_config["title"],
                        self._get_datatype_factory().get_instance(node.datatype).get_display_value(tile, node))
        return return_value


    def _get_value_from_node(self, name_node, resourceinstanceid):

        tile = models.TileModel.objects.filter(
            nodegroup_id=name_node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()
        if not tile:
            return None
        datatype = self._get_datatype_factory().get_instance(name_node.datatype)
        return datatype.get_display_value(tile, name_node)

    def _get_datatype_factory(self):
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
        return self._datatype_factory

    # def _get_sample_values(self, resource, values_config):
    #     # print("Resource: %s" % resource.resourceinstanceid)
    #     return_values = {}
    #
    #     fossil_sample_values = models.ResourceXResource.objects.filter(
    #         resourceinstanceidfrom=resource.resourceinstanceid,
    #         nodeid=BCFossilSampleDescriptors._collected_fossils_node.nodeid
    #     ).values_list('resourceinstanceidto', flat=True)
    #
    #     for child_values in values_config:
    #         tiles = models.TileModel.objects.filter(
    #             nodegroup_id=child_values["node"].nodegroup_id,
    #             resourceinstance_id__in=fossil_sample_values
    #         ).all()
    #
    #         if len(tiles) != 0:
    #             datatype = self._get_datatype_factory().get_instance(child_values["node"].datatype)
    #
    #             values = []
    #             for tile in tiles:
    #                 period_value = datatype.get_display_value(tile, child_values["node"])
    #                 if period_value:
    #                     values.append(period_value)
    #
    #             if len(values) > 0:
    #                 return_values[child_values["label"]] = ', '.join(list(set(values)))
    #     return return_values

    def _get_site_name(self, resource):
        for alias in BCFossilSampleDescriptors._sample_name_nodes:
            value = self._get_value_from_node(
                BCFossilSampleDescriptors._nodes[alias], resource.resourceinstanceid
            )
            if value:
                return value
        return "No reference"

    def _format_value(self, name, value):
        return "" if not value else "<dt>%s</dt><dd>%s</dd>" % (name, value)

    def _nodeid_to_sequence(self, id_list, row):
        return id_list.index(row.nodeid)
