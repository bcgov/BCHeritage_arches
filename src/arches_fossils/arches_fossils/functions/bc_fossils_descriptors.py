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
    "defaultconfig": {"module": "arches_fossils.functions.bc_fossils_descriptors", "class_name": "BCFossilsDescriptors",
                      "descriptor_types": {
                          "name": {"type": "name"},
                          "description": {"type": "description"},
                          "map_popup": {"type": "map_popup"}
                      },
                      "triggering_nodegroups": []},
    "classname": "BCFossilsDescriptors",
    "component": "views/components/functions/bc-fossils-descriptors",
}


class BCFossilsDescriptors(AbstractPrimaryDescriptorsFunction):
    def get_primary_descriptor_from_nodes(self, resource, config):
        # print(str(config))
        try:
            if config["type"] == "name":
                return self.get_name(resource, config, ["Fossil Type", "Fossil Common Names"])
            elif config["type"] == "description":
                return self.get_name(resource, config, ["Fossil Common Names"])
            elif config["type"] == "map_popup":
                return self.get_map_popup(resource, config)
            else:
                pass
        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def get_name(self, resource, config, names):
        datatype_factory = DataTypeFactory()
        try:
            for name in names:
                name_nodes = models.Node.objects.filter(name=name)
                if len(name_nodes) == 0:
                    print("invalid node name %s in type %s" % (name, config["type"]))
                    continue
                name_node = name_nodes[0]
                tiles = models.TileModel.objects.filter(nodegroup_id=name_node.nodegroup_id).filter(
                    resourceinstance_id=resource.resourceinstanceid
                )
                if not datatype_factory:
                    datatype_factory = DataTypeFactory()

                datatype = datatype_factory.get_instance(name_node.datatype)
                value = datatype.get_display_value(tiles[0], name_node)
                if value and value != 'None':
                    return value

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def get_description(self, resource, config):
        return "Description"

    def get_map_popup(self, resource, config):
        return "Map Popup"
        # try:
        #     if "nodegroup_id" in config and config["nodegroup_id"] != "" and config["nodegroup_id"] is not None:
        #         template = config["string_template"]
        #         sci_name_nodes = models.Node.objects.filter( name="Fossil Type" )
        #         sci_name_node = sci_name_nodes[0]
        #         print ("Scientific Name Nodegroup ID %s" % str(sci_name_node.nodegroup_id))
        #         print ("Resource: %s", str(resource))
        #
        #         tiles = models.TileModel.objects.filter(nodegroup_id=sci_name_node.nodegroup_id).filter( resourceinstance_id=resource.resourceinstanceid )
        #
        #         print("Config %s", str(config))
        #         print("Tiles %s", len(tiles))
        #         print ("Borden Number %s" % str(sci_name_node.nodegroup_id))
        #
        #         if len(tiles) > 0:
        #             if not datatype_factory:
        #                 datatype_factory = DataTypeFactory()
        #             datatype = datatype_factory.get_instance(sci_name_node.datatype)
        #             value = datatype.get_display_value(tiles[0], sci_name_node)
        #             print ("Scientific name: %s" % value)
        #
        #
        #         # return tiles.tiledata[borden_number_node.nodeid]
        #
        #
        #         tiles = models.TileModel.objects.filter(nodegroup_id=uuid.UUID(config["nodegroup_id"]), sortorder=0).filter(
        #                 resourceinstance_id=resource.resourceinstanceid
        #             )
        #         if len(tiles) == 0:
        #             tiles = models.TileModel.objects.filter(nodegroup_id=uuid.UUID(config["nodegroup_id"])).filter(
        #                 resourceinstance_id=resource.resourceinstanceid
        #             )
        #         for tile in tiles:
        #             for node in models.Node.objects.filter(nodegroup_id=uuid.UUID(config["nodegroup_id"])):
        #                 print("ID: %s, Name: %s, Tile Data length: %s" % (str(node.nodeid), str(node.name), str(tile.data.keys())))
        #                 data = {}
        #                 if len(list(tile.data.keys())) > 0:
        #                     data = tile.data
        #                 elif tile.provisionaledits is not None and len(list(tile.provisionaledits.keys())) == 1:
        #                     userid = list(tile.provisionaledits.keys())[0]
        #                     data = tile.provisionaledits[userid]["value"]
        #                 # if node.name == "BC Right":
        #                 #     print(str(node.nodeid))
        #                 #     print(config["string_template"])
        #                 #     print(str(data))
        #                 #     print("\tTile data %s"%str(tile.data))
        #                 #     print(str(str(node.nodeid) in data))
        #                 if str(node.nodeid) in data:
        #                     # print(str(node.name))
        #                     if not datatype_factory:
        #                         datatype_factory = DataTypeFactory()
        #                     datatype = datatype_factory.get_instance(node.datatype)
        #                     value = datatype.get_display_value(tile, node)
        #                     if value is None:
        #                         value = ""
        #                     config["string_template"] = config["string_template"].replace("<%s>" % node.name, str(value)+str(2))
        # except ValueError as e:
        #     print(e, "invalid nodegroupid participating in descriptor function.")
        # if config["string_template"].strip() == "":
        #     config["string_template"] = _("Undefined")
        # # print(str(config))
        # return config["string_template"]+"HI"
