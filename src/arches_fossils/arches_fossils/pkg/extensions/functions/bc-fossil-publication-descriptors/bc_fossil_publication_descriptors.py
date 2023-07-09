from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _

details = {
    "functionid": "60000000-0000-0000-0000-000000001003",
    "name": "Publication Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossil_publication_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Fossils resources",
    "defaultconfig": {
        "module": "arches_fossils.functions.bc_fossil_publication_descriptors",
        "class_name": "BCFossilsPublicationDescriptors",
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
    "classname": "BCFossilPublicationDescriptors",
    "component": "views/components/functions/bc-fossil-publication-descriptors",
}


class BCFossilPublicationDescriptors(AbstractPrimaryDescriptorsFunction):
    _graph_name = {"en": "Publication"}
    _datatype_factory = None

    _title_node = None
    _publication_type_node = None
    _journal_or_publication_name = None

    _collected_fossils_node = None
    _collection_event_graph_id = None
    _coll_event_samples_values_config = None
    _coll_event_popup_order = ["Detailed Location", "Formation", "Period", "Samples Collected"]
    _coll_event_card_order = ["Detailed Location", "Period", "Samples Collected"]

    @staticmethod
    def initialize_static_data():
        BCFossilPublicationDescriptors._title_node = models.Node.objects.filter(
            alias='title',
            graph__name__contains=BCFossilPublicationDescriptors._graph_name
        ).first()

        BCFossilPublicationDescriptors._publication_type_node = models.Node.objects.filter(
            alias='publication_type',
            graph__name__contains=BCFossilPublicationDescriptors._graph_name
        ).first()

        BCFossilPublicationDescriptors._journal_or_publication_name = models.Node.objects.filter(
            alias="journal_or_publication_name",
            graph__name__contains=BCFossilPublicationDescriptors._graph_name
        ).first()

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        return_value = None
        display_values = {}
        # print("get_primary_descriptor_from_nodes")

        if BCFossilPublicationDescriptors._title_node is None:
            BCFossilPublicationDescriptors.initialize_static_data()

        try:
            # print("Type: %s" % config["type"])
            if config["type"] == "name":
                return self._get_name(resource)

            return self._format_value(
                "Publication Type", self._get_value_from_node(BCFossilPublicationDescriptors._publication_type_node, resource,
                                                              ), {"show_name": True})
        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

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

    def _get_name(self, resource):
        parent_publication_name = ""

        publication_type = self._get_value_from_node(BCFossilPublicationDescriptors._publication_type_node, resource)
        if publication_type == "Volume / Publication Number":
            parent_publication_name = self._get_value_from_node(BCFossilPublicationDescriptors._journal_or_publication_name, resource) + " "
        title = self._get_value_from_node(BCFossilPublicationDescriptors._title_node, resource)

        return parent_publication_name + title

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value
