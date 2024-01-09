from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models


class BCPrimaryDescriptorsFunction(AbstractPrimaryDescriptorsFunction):
    display_pattern = "<dt>%s</dt><dd>%s</dd>"

    def format_value(self, name, value, show_name=True):
        if type(value) is list:
            value = set(value)
            if "" in value:
                value.remove("")
            value = ", ".join(sorted(value))

        if value is None:
            return ""
        elif show_name:
            return self.display_pattern % (name, value)
        return value

    def get_value_from_node(self, node, datatype, resourceinstanceid=None, data_tile=None):
        """
        get the display value from the resource tile(s) for the node with the given name

        Keyword Arguments

        node     -- node of the data to extract
        datatype -- datatype that can be used to extract the data from the tile
        resourceinstanceid -- id of resource instance used to fetch the tile(s) if data_tile not specified
        data_tile -- if specified, the tile to extract the value from
        """

        if node is None or datatype is None:
            return None

        display_values = []

        tiles = [data_tile] if data_tile else models.TileModel.objects.filter(
            nodegroup_id=node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid)
        print("Tiles: %s" % len(tiles))

        for tile in tiles:
            if tile:
                display_values.append(
                    datatype.get_display_value(tile, node))
        print("%s -> %s" % (node.name, display_values))

        return None if len(display_values) == 0 else (display_values[0] if len(display_values) == 1 else display_values)
