from arches.app.models import models
from bcfms.util.bcfms_aliases import (
    GraphSlugs,
    CollectionEventAliases,
    FossilSampleAliases,
    IPA,
)
from bcfms.util.scientific_terms_util import ScientificTermsFormatter
from bcgov_arches_common.util.graph_lookup import GraphLookup
from arches.settings import LANGUAGE_CODE
from datetime import date
import re


class BusinessDataProxy:

    _graph_lookup = None

    def __init__(self, graph_slug, node_aliases):
        self._graph_lookup = GraphLookup(graph_slug, node_aliases)

    def get_value_from_node(
        self,
        alias,
        resourceinstanceid=None,
        data_tile=None,
        context=None,
        use_boolean_label=True,
    ):
        """
        get the values from the resource tile(s) for the node with the given name

        Keyword Arguments

        alias     -- node alias of the data to extract
        resourceinstanceid -- id of resource instance used to fetch the tile(s) if data_tile not specified
        data_tile -- if specified, the tile to extract the value from
        context -- if specified, context with the target language
        use_boolean_label -- If true, for boolean datatypes, returns the associated label, otherwise use raw value
        """
        node = self._graph_lookup.get_node(alias)
        datatype = self._graph_lookup.get_datatype(alias)

        if node is None or datatype is None:
            return None

        display_values = []

        if context is not None and "language" in context:
            language = context["language"]
        else:
            language = LANGUAGE_CODE

        tiles = (
            [data_tile]
            if data_tile
            else models.TileModel.objects.filter(nodegroup_id=node.nodegroup_id).filter(
                resourceinstance_id=resourceinstanceid
            )
        )
        # print("Tiles: %s" % len(tiles))

        for tile in tiles:
            if tile:
                if (
                    node.datatype == "boolean"
                    and use_boolean_label
                    and "trueLabel" in node.config
                ):
                    value = (datatype.get_tile_data(tile))[str(node.nodeid)]
                    if value is None:
                        return None
                    else:
                        display_values.append(
                            node.config["trueLabel"][language]
                            if (datatype.get_tile_data(tile))[str(node.nodeid)]
                            else node.config["falseLabel"][language]
                        )
                else:
                    display_values.append(
                        datatype.get_display_value(tile, node, language=language)
                    )
        # print("%s -> %s" % (node.name, display_values))
        return (
            None
            if len(display_values) == 0
            else (display_values[0] if len(display_values) == 1 else display_values)
        )


class FossilSampleDataProxy(BusinessDataProxy):

    def __init__(self):
        super(FossilSampleDataProxy, self).__init__(
            GraphSlugs.FOSSIL_SAMPLE, FossilSampleAliases.get_aliases().values()
        )

    def get_values_from_samples(
        self, samples, node_alias, uncertainty_alias=None, flatten=False
    ):
        values = []
        for sample in samples:
            if uncertainty_alias is None:
                next_value = self.get_value_from_node(
                    node_alias, resourceinstanceid=sample
                )
            else:
                next_value = ScientificTermsFormatter.format_uncertain(
                    self.get_value_from_node(node_alias, resourceinstanceid=sample),
                    self.get_value_from_node(
                        uncertainty_alias,
                        resourceinstanceid=sample,
                        use_boolean_label=False,
                    ),
                )
            values += (
                next_value if type(next_value) is list and flatten else [next_value]
            )
            # values.append(self.get_value_from_node(node_alias, resourceinstanceid=sample))
        # values = [val for val in values if val is not None and val != ""]
        # print("Node alias: %s values: %s" % (node_alias, values))
        # return "" if len(values) == 0 else self.format_value(label, values)
        return values

    def get_scientific_names_from_samples(self, samples):
        values = []
        # sample_ids = list(map(lambda sample: sample.resourceinstanceid, samples))
        sample_ids = samples
        tiles = models.TileModel.objects.filter(
            nodegroup_id=self._graph_lookup.get_node(
                FossilSampleAliases.SCIENTIFIC_NAME
            ).nodegroup_id,
            resourceinstance_id__in=sample_ids,
        ).all()
        for tile in tiles:
            values.append(
                ScientificTermsFormatter.format_scientific_name(
                    self.get_value_from_node(
                        FossilSampleAliases.SCIENTIFIC_NAME, data_tile=tile
                    ),
                    self.get_value_from_node(
                        FossilSampleAliases.NAME_CONNECTOR, data_tile=tile
                    ),
                    self.get_value_from_node(
                        FossilSampleAliases.OTHER_SCIENTIFIC_NAME, data_tile=tile
                    ),
                )
            )
        values = list(filter(lambda val: val is not None, values))
        values.sort()
        return values

    def get_common_names_from_samples(self, samples):
        values = []
        sample_ids = samples
        tiles = models.TileModel.objects.filter(
            nodegroup_id=self._graph_lookup.get_node(
                FossilSampleAliases.FOSSIL_COMMON_NAME
            ).nodegroup_id,
            resourceinstance_id__in=sample_ids,
        ).all()
        for tile in tiles:
            values.append(
                ScientificTermsFormatter.format_uncertain(
                    self.get_value_from_node(
                        FossilSampleAliases.FOSSIL_COMMON_NAME, data_tile=tile
                    ),
                    self.get_value_from_node(
                        FossilSampleAliases.COMMON_NAME_UNCERTAIN, data_tile=tile
                    ),
                )
            )
        values = list(filter(lambda val: val is not None, values))
        values.sort()
        return values


class CollectionEventDataProxy(BusinessDataProxy):

    def __init__(self):
        super(CollectionEventDataProxy, self).__init__(
            GraphSlugs.COLLECTION_EVENT, CollectionEventAliases.get_aliases().values()
        )

    def get_sample_ids(self, collection_event_id):
        return models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=collection_event_id,
            nodeid=self._graph_lookup.get_node(
                CollectionEventAliases.SAMPLES_COLLECTED
            ).nodeid,
        ).values_list("resourceinstanceidto", flat=True)


class IPADataProxy(BusinessDataProxy):

    def __init__(self):
        super(IPADataProxy, self).__init__(
            GraphSlugs.PROJECT_ASSESSMENT, IPA.get_aliases().values()
        )

    @staticmethod
    def get_last_report_id(node_id, report_type_abbreviation):
        # Gets the next report number in the sequence.
        # Assumes that there is only one report type abbreviation for any particular node
        # Report number format is <year>-<abbreviation>-<seq#> eg: 2024-PSR-001
        current_year = str(date.today().year)

        node = models.Node.objects.get(nodeid=node_id)
        tiles = (
            models.TileModel.objects.filter(nodegroup_id=node.nodegroup_id)
            .values_list("data", flat=True)
            .all()
        )
        values = sorted(
            list(
                map(
                    lambda tile: (
                        tile[node_id]["en"]["value"] if tile[node_id] else None
                    ),
                    tiles,
                )
            ),
            reverse=True,
        )

        if len(values) < 1 or not re.match(r"^%s" % current_year, values[0]):
            return "%s-%s-001" % (current_year, report_type_abbreviation)
        else:
            val = "{:0=3}".format(int(re.split("-", values[0])[2]) + 1)
            return re.sub("[^-]{3}$", val, values[0])
