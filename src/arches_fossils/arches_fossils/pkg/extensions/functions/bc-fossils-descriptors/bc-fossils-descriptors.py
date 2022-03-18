import uuid
from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.models.tile import Tile
from arches.app.models.models import Node
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _

details = {
    "name": "BC Fossils Descriptors",
    "type": "primarydescriptors",
    "description": "Function that provides the primary descriptors for BC Fossils resources",
    "defaultconfig": {
        "module": "arches_fossils.functions.bc_fossils_descriptors",
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


class BCFossilsDescriptors(AbstractPrimaryDescriptorsFunction):
    def get_primary_descriptor_from_nodes(self, resource, config):
        datatype_factory = DataTypeFactory()
        return_value = None
        try:
            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                nodeid__in=config['node_ids']
            )
            for name_node in name_nodes:
                # if len(name_nodes) == 0:
                #     print("invalid node ID %s in type %s" % (nodeid, config["type"]))
                #     continue
                # name_node = name_nodes[0]
                tiles = models.TileModel.objects.filter(
                    nodegroup_id=name_node.nodegroup_id
                ).filter(resourceinstance_id=resource.resourceinstanceid)
                if not datatype_factory:
                    datatype_factory = DataTypeFactory()
                if len(tiles) == 0:
                    continue

                datatype = datatype_factory.get_instance(name_node.datatype)
                value = datatype.get_display_value(tiles[0], name_node)
                if value and value != "None":
                    if config["first_only"]:
                        return self._format_value(name_node.name, value, config)
                    else:
                        if config["delimiter"] and return_value:
                            return_value += config["delimiter"]
                        elif not return_value:
                            return_value = ""
                        return_value += self._format_value(name_node.name, value, config)
            return return_value
        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value
