from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.settings import LANGUAGE_CODE


class BCPrimaryDescriptorsFunction(AbstractPrimaryDescriptorsFunction):
    display_pattern = "<dt>%s</dt><dd>%s</dd>"

    def format_values(self, graph_lookup, node_aliases, resource):
        return_value = ""
        for node_alias in node_aliases:
            value = self.get_value_from_node(
                    graph_lookup.get_node(node_alias),
                    graph_lookup.get_datatype(node_alias),
                    resource)
            if value:
                return_value += self.format_value(
                    graph_lookup.get_node(node_alias).name,
                    value, True)

        return return_value

    def format_value(self, name, value, show_name=True, value_connector=", ", unique_list=True):
        if type(value) is list:
            value = [val for val in value if val is not None and val != ""]
            if unique_list:
                value = list(set(value))

        if value is None or value == "" or type(value) is list and len(value) == 0:
            return ""
        elif show_name:
            return self.display_pattern % (name, value_connector.join(value) if type(value) is list else value)
        return value_connector.join(value) if type(value) is list else value

    def get_value_from_node(self, node, datatype, resourceinstanceid=None, data_tile=None, context=None, use_boolean_label=True):
        """
        get the display value from the resource tile(s) for the node with the given name

        Keyword Arguments

        node     -- node of the data to extract
        datatype -- datatype that can be used to extract the data from the tile
        resourceinstanceid -- id of resource instance used to fetch the tile(s) if data_tile not specified
        data_tile -- if specified, the tile to extract the value from
        context -- if specified, context with the target language
        use_boolean_label -- If true, for boolean datatypes, returns the associated label, otherwise use raw value
        """

        if node is None or datatype is None:
            return None

        display_values = []

        if context is not None and "language" in context:
            language = context["language"]
        else:
            language = LANGUAGE_CODE

        tiles = [data_tile] if data_tile else models.TileModel.objects.filter(
            nodegroup_id=node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid)
        # print("Tiles: %s" % len(tiles))

        for tile in tiles:
            if tile:
                if node.datatype == "boolean" and use_boolean_label and 'trueLabel' in node.config:
                    value = (datatype.get_tile_data(tile))[str(node.nodeid)]
                    if value is None:
                        return None
                    else:
                        display_values.append(node.config['trueLabel'][language] if (datatype.get_tile_data(tile))[
                            str(node.nodeid)] else node.config['falseLabel'][language])
                else:
                    display_values.append(
                        datatype.get_display_value(tile, node, language=language))
        # print("%s -> %s" % (node.name, display_values))
        return None if len(display_values) == 0 else (display_values[0] if len(display_values) == 1 else display_values)
