from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from arches.settings import LANGUAGE_CODE

from django.utils.translation import ugettext as _

details = {
    "functionid": "60000000-0000-0000-0000-000000001002",
    "name": "BC Fossil Type Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossil_type_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Fossil Type resources",
    "defaultconfig": {
        "module": "arches_fossils.functions.bc_fossil_type_descriptors",
        "class_name": "BCFossilTypeDescriptors",
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
    "classname": "BCFossilTypeDescriptors",
    "component": "views/components/functions/bc-fossil-type-descriptors",
}


class BCFossilTypeDescriptors(AbstractPrimaryDescriptorsFunction):
    _type_graph_name = {"en": "BC Fossil Type"}
    _datatype_factory = None
    _parent_name_node = None
    _taxonomic_rank_node = None
    _name_node = None
    _fossil_type_graph_id = None

    _coll_event_samples_values_config = None
    _card_order = ["Size Category", "Default Significance"]

    @staticmethod
    def initialize_static_data():
        BCFossilTypeDescriptors._name_node = models.Node.objects.filter(
            alias='name',
            graph__name__contains=BCFossilTypeDescriptors._type_graph_name
        ).first()
        BCFossilTypeDescriptors._parent_name_node = models.Node.objects.filter(
            alias='parent_name',
            graph__name__contains=BCFossilTypeDescriptors._type_graph_name
        ).first()
        BCFossilTypeDescriptors._taxonomic_rank_node = models.Node.objects.filter(
            alias='taxonomic_rank',
            graph__name__contains=BCFossilTypeDescriptors._type_graph_name
        ).first()

        BCFossilTypeDescriptors._fossil_type_graph_id = \
            models.GraphModel.objects.filter(name=BCFossilTypeDescriptors._type_graph_name).filter(isresource=True).values(
                "graphid").first()["graphid"]

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        if BCFossilTypeDescriptors._name_node is None:
            BCFossilTypeDescriptors.initialize_static_data()

        try:
            if config["type"] == "name":
                return self._get_name(resource, context)
            else:

                tmp_node = models.Node.objects.filter(
                    alias='size_category',
                    graph__name__contains=BCFossilTypeDescriptors._type_graph_name
                ).first()
                return_value = self._get_value_from_node(tmp_node, resource.resourceinstanceid, context)

                if return_value is None:
                    return_value = ""
                return_value += "<br>"

                tmp_node = models.Node.objects.filter(
                    alias='default_significance',
                    graph__name__contains=BCFossilTypeDescriptors._type_graph_name
                ).first()
                tmp_value = self._get_value_from_node(tmp_node, resource.resourceinstanceid, context)

                if tmp_value is not None:
                    return_value += tmp_value
                return return_value if return_value is not None else ""

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_value_from_node(self, name_node, resourceinstanceid, context):

        tile = models.TileModel.objects.filter(
            nodegroup_id=name_node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()
        if not tile:
            # print("No tile")
            return None
        # print("Name Node Config: %s " % str(name_node.config))
        # print("Name Node ID: %s " % str(name_node.nodeid))
        # print("Name Node Datatype: %s " % str(name_node.datatype))
        #
        # print("Tile: %s " % str(tile))
        datatype = self._get_datatype_factory().get_instance(name_node.datatype)
        # print("Datatype 2: %s" % datatype)
        language = None
        # print("Datatype tile data: %s" % datatype.get_tile_data(tile))
        if context is not None and "language" in context:
            language = context["language"]
        else:
            language = LANGUAGE_CODE

        if name_node.datatype == "boolean" and 'trueLabel' in name_node.config:
            value = (datatype.get_tile_data(tile))[str(name_node.nodeid)]
            if value is None:
                return None
            else:
                return name_node.config['trueLabel'][language] if (datatype.get_tile_data(tile))[
                    str(name_node.nodeid)] else \
                    name_node.config['falseLabel'][language]

        display_value = datatype.get_display_value(tile, name_node, language=language)
        # print("Display value: %s" % display_value)
        return display_value if display_value is not None else ""

    def _get_datatype_factory(self):
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
        return self._datatype_factory

    def _get_parent_name(self, resource, context):
        # print("Resource: %s" % resource.resourceinstanceid)

        parent_value = models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=resource.resourceinstanceid,
            nodeid=BCFossilTypeDescriptors._parent_name_node.nodeid
        ).first()

        return self._get_value_from_node(self._name_node, parent_value.resourceinstanceidto, context)

    def _get_name(self, resource, context):
        display_value = ""
        taxonomic_rank = self._get_value_from_node(
            self._taxonomic_rank_node, resource.resourceinstanceid, context
        )
        if taxonomic_rank == 'Species':
            display_value = self._get_parent_name(resource, context)+" "

        display_value += self._get_value_from_node(
            self._name_node, resource.resourceinstanceid, context
        )

        return display_value

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value
