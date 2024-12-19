from bcfms.util.bcfms_aliases import GraphSlugs, PublicationAliases as aliases
from bcgov_arches_common.util.bc_primary_descriptors_function import BCPrimaryDescriptorsFunction
from bcgov_arches_common.util.graph_lookup import GraphLookup

details = {
    "functionid": "60000000-0000-0000-0000-000000001003",
    "name": "Publication Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossil_publication_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Fossils resources",
    "defaultconfig": {
        "module": "bcfms.functions.bc_fossil_publication_descriptors",
        "class_name": "BCFossilsPublicationDescriptors",
        "descriptor_types": {
            "name": {
            },
            "description": {
            },
            "map_popup": {
            },
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCFossilPublicationDescriptors",
    "component": "views/components/functions/bc-fossil-publication-descriptors",
}


class BCFossilPublicationDescriptors(BCPrimaryDescriptorsFunction):
    # For Name part of descriptor
    _graph_slug = GraphSlugs.PUBLICATION
    _graph_lookup = None

    _name_nodes = [aliases.TITLE, aliases.JOURNAL_OR_PUBLICATION_NAME]
    _card_nodes = [aliases.AUTHORS, aliases.PUBLICATION_TYPE]

    def __init__(self):
        super(BCFossilPublicationDescriptors).__init__()
        self._graph_lookup = GraphLookup(BCFossilPublicationDescriptors._graph_slug, BCFossilPublicationDescriptors._name_nodes + BCFossilPublicationDescriptors._card_nodes)

    def get_primary_descriptor_from_nodes(self, resource, config, context=None, descriptor=None):
        return_value = ""

        try:
            if descriptor == "name":
                return self._get_name(resource)

            for node_alias in self._card_nodes:
                value = self.get_value_from_node(
                    self._graph_lookup.get_node(node_alias),
                    self._graph_lookup.get_datatype(node_alias),
                    resource)
                if value:
                    return_value += self.format_value(
                        self._graph_lookup.get_node(node_alias).name,
                        value, True)

            return return_value

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_name(self, resource):
        parent_publication_name = ""

        publication_type = self.get_value_from_node(
            self._graph_lookup.get_node(aliases.PUBLICATION_TYPE),
            self._graph_lookup.get_datatype(aliases.PUBLICATION_TYPE),
            resource)
        if publication_type == "Volume / Publication Number":
            parent_publication_name = \
                "%s " % self.get_value_from_node(self._graph_lookup.get_node(aliases.JOURNAL_OR_PUBLICATION_NAME),
                                                 self._graph_lookup.get_datatype(aliases.JOURNAL_OR_PUBLICATION_NAME),
                                                 resource)

        title = self.get_value_from_node(
            self._graph_lookup.get_node(aliases.TITLE),
            self._graph_lookup.get_datatype(aliases.TITLE),
            resource)

        # print("Resource: %s, Title: %s, Parent: %s" % (resource, title, parent_publication_name))
        # This shouldn't be necessary but we have some cardinality violations
        return parent_publication_name + str(title)
