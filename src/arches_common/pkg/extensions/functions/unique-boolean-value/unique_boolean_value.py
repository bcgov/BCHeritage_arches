import uuid
from django.core.exceptions import ValidationError
from arches.app.functions.base import BaseFunction
from arches.app.models import models
from arches.app.models.tile import Tile
from arches.app.datatypes.datatypes import BooleanDataType
from django.db.models import Q
from arches.app.models.tile import TileValidationError
import json

details = {
    "functionid": "60000000-0000-0000-0000-000000002001",
    "name": "Unique Boolean Value",
    "type": "node",
    "modulename": "unique_boolean_value.py",
    "description": "Enforces that only one card is set to the boolean value for a resource",
    "defaultconfig": {"node_id": "", "unique_value": True, "triggering_nodegroups": []},
    "classname": "UniqueBooleanValue",
    "component": "views/components/functions/unique-boolean-value",
}


class UniqueBooleanValue(BaseFunction):
    def save(self, tile, request):
        # print("running before tile save")
        data = tile.data
        node_id = self.config["node_id"]
        node_value = data[node_id]

        datatype = BooleanDataType()
        # node_id = self.config["triggering_nodegroups"][0]
        if datatype.values_match(self.config["unique_value"], node_value):
            other_tiles = models.TileModel.objects.filter(
                Q(resourceinstance=tile.resourceinstance),
                Q(nodegroup_id=self.config["triggering_nodegroups"][0]),
                ~Q(tileid=tile.tileid))
            if len(other_tiles) > 0:
                for other_tile in other_tiles:
                    if datatype.values_match(node_value, other_tile.data[node_id]):
                        node = models.Node.objects.get(pk=node_id)
                        raise TileValidationError("%s must be unique within all %s values" % (node_value, node.name))
            # else:
            #     print("Why are we here?")

    def post_save(self, tile, request, context):
        pass

    def on_import(self, tile, request):
        print("calling on import")

    def get(self, tile, request):
        print("calling get")

    def delete(self, tile, request):
        print("calling delete")
