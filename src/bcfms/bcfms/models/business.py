from django.contrib.gis.db import models
from arches.app.models.resource import Resource
from arches.app.models.tile import Tile
from arches.app.models.models import Node
from bcfms.util.bcfms_aliases import GraphSlugs, IPA as IPA_aliases
from arches.app.models.resource import parse_node_value
from arches.app.utils.exceptions import MultipleNodesFoundException


class IPA(Resource):

    class Meta:
        proxy = True

    def __init__(self, *args, **kwargs):
        super(IPA, self).__init__(*args, **kwargs)

    def get_all_resources(self):
        return Resource.objects.filter(graph=GraphSlugs.PROJECT_ASSESSMENT)

    def get_tile_for_nodegroup(self, nodegroupid):
        super().load_tiles()
        return next(tile for tile in self.tiles if tile.nodegroup__id == nodegroupid)

    def get_node_values_by_alias(self, alias):
        """
        Take a node_name (string) as an argument and return a list of values.
        If an invalid node_name is used, or if multiple nodes with the same
        name are found, the method returns False.
        Current supported (tested) node types are: string, date, concept, geometry
        """

        nodes = Node.objects.filter(alias=alias, graph_id=self.graph_id)
        if len(nodes) > 1:
            raise MultipleNodesFoundException(alias, nodes)

        if len(nodes) == 0:
            raise InvalidNodeAliasException(alias)

        tiles = self.tilemodel_set.filter(nodegroup_id=nodes[0].nodegroup_id)

        values = []
        for tile in tiles:
            for node_id, value in tile.data.items():
                if node_id == str(nodes[0].nodeid):
                    if type(value) is list:
                        for v in value:
                            values.append(parse_node_value(v))
                    else:
                        values.append(parse_node_value(value))

        return values

    def get_project_name(self):
        return self.get_node_values_by_alias(IPA_aliases.PROJECT_NAME)
        # super().get_node_values(node_name="Project Description")
        # print (self.tiles)
        # return self.tiles


    def save_project(self, project_data: object):
        # {"project_name": "ABC 123",
        #
        #
        #
        #
        # }
        pass



class InvalidNodeAliasException(Exception):
    def __init__(self, name):
        self.message = "Node with the alias '%s' doesn't exist" % name


