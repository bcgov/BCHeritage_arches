from arches.app.models import models
from bcgov_arches_common.util.bc_primary_descriptors_function import (
    BCPrimaryDescriptorsFunction,
)
from bcgov_arches_common.util.graph_lookup import GraphLookup
from bcfms.util.bcfms_aliases import GraphSlugs, FossilType as aliases

details = {
    "functionid": "60000000-0000-0000-0000-000000001002",
    "name": "Fossil Type Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossil_type_descriptors.py",
    "description": "Function that provides the primary descriptors for Fossil Type resources",
    "defaultconfig": {
        "module": "bcfms.functions.bc_fossil_type_descriptors",
        "class_name": "BCFossilTypeDescriptors",
        "descriptor_types": {
            "name": {},
            "description": {},
            "map_popup": {},
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCFossilTypeDescriptors",
    "component": "views/components/functions/bc-fossil-type-descriptors",
}


class BCFossilTypeDescriptors(BCPrimaryDescriptorsFunction):
    _graph_slug = GraphSlugs.FOSSIL_TYPE
    _graph_lookup = None

    _name_nodes = [aliases.NAME, aliases.PARENT_NAME, aliases.TAXONOMIC_RANK]
    _card_nodes = [aliases.NAME_TYPE, aliases.SIZE_CATEGORY]

    def __init__(self):
        super(BCFossilTypeDescriptors).__init__()
        self._graph_lookup = GraphLookup(
            BCFossilTypeDescriptors._graph_slug,
            BCFossilTypeDescriptors._name_nodes + BCFossilTypeDescriptors._card_nodes,
        )

    def get_primary_descriptor_from_nodes(
        self, resource, config, context=None, descriptor=None
    ):
        try:
            if descriptor == "name":
                return self._get_name(resource, context)
            else:
                return self.format_values(
                    graph_lookup=self._graph_lookup,
                    node_aliases=self._card_nodes,
                    resource=resource.resourceinstanceid,
                )

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_parent_name(self, resource, context):
        parent_value = self.get_value_from_node(
            self._graph_lookup.get_node(aliases.PARENT_NAME),
            self._graph_lookup.get_datatype(aliases.PARENT_NAME),
            resource,
        )
        return "" if not parent_value else parent_value

    def _get_name(self, resource, context):
        display_value = ""
        taxonomic_rank = self.get_value_from_node(
            node=self._graph_lookup.get_node(aliases.TAXONOMIC_RANK),
            datatype=self._graph_lookup.get_datatype(aliases.TAXONOMIC_RANK),
            resourceinstanceid=resource.resourceinstanceid,
            context=context,
        )
        if taxonomic_rank == "Species":
            display_value = self._get_parent_name(resource, context) + " "

        name = self.get_value_from_node(
            node=self._graph_lookup.get_node(aliases.NAME),
            datatype=self._graph_lookup.get_datatype(aliases.NAME),
            resourceinstanceid=resource.resourceinstanceid,
            context=context,
        )
        display_value += name if name else ""

        return display_value.strip()
