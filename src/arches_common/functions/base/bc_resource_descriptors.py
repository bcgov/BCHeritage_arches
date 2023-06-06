from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory


class BCResourceDescriptors(AbstractPrimaryDescriptorsFunction):
    """
    Base class for BC Primary Descriptors functions. Has common functionality
    to cache Nodes and DataTypes, to extract data from the Tiles and to format
    the values for display.
    """
    _datatype_factory = DataTypeFactory()

    # For Name part of descriptor
    en_graph = {"en": ""}

    _nodes = {}
    _datatypes = {}

    _initialized = False

    # Initializes the static nodes and datatypes data
    def initialize(self, node_aliases):
        for alias in node_aliases:
            node = models.Node.objects.filter(
                alias=alias,
                graph__name__contains=BCResourceDescriptors.en_graph
            ).first()
            if node:
                BCResourceDescriptors._nodes[alias] = node
                BCResourceDescriptors._datatypes[alias] = BCResourceDescriptors._datatype_factory.get_instance(
                    node.datatype)

        BCResourceDescriptors._initialized = True

    @staticmethod
    def _get_value_from_node(node_alias, resourceinstanceid=None, data_tile=None):
        """
        get the display value from the resource tile(s) for the node with the given name

        Keyword Arguments

        node_alias -- node alias of the data to extract
        resourceinstanceid -- id of resource instance used to fetch the tile(s) if data_tile not specified
        data_tile -- if specified, the tile to extract the value from
        """
        if node_alias not in BCResourceDescriptors._nodes:
            return None

        display_values = []
        datatype = BCResourceDescriptors._datatypes[node_alias]

        tiles = [data_tile] if data_tile else models.TileModel.objects.filter(
            nodegroup_id=BCResourceDescriptors._nodes[node_alias].nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid)

        for tile in tiles:
            if tile:
                display_values.append(datatype.get_display_value(tile, BCResourceDescriptors._nodes[node_alias]))

        return None if len(display_values) == 0 else (display_values[0] if len(display_values) == 1 else display_values)

    @staticmethod
    def _format_value(name, value, config):
        if type(value) is list:
            value = set(value)
            if "" in value:
                value.remove("")
            value = ", ".join(sorted(value))

        if value is None:
            return ""
        elif config["show_name"]:
            return "<div class='bc-popup-entry'><div class='bc-popup-label'>%s</div><div class='bc-popup-value'>%s</div></div>" % (
            name, value)
        return value
