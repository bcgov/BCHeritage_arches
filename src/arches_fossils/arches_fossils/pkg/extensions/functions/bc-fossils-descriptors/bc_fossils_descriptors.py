import json
import uuid
from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.models.tile import Tile
from arches.app.models.models import Node
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _

details = {
    "functionid": "60000000-0000-0000-0000-000000001001",
    "name": "BC Fossils Descriptors",
    "type": "primarydescriptors",
    "modulename": "bc_fossils_descriptors.py",
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
    _datatype_factory = None
    _formation_node = None
    _geologic_period_node = None
    _collected_fossils_node = None

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        return_value = None
        try:
            # print("Config: %s" % config)
            # print("Context: %s" % context)
            # print("Resource: %s" % resource)
            # Name for CollectionEvent is a special case
            if str(resource.graph_id) == "df3ee1ae-9c1c-11ec-964d-5254008afee6" and config["type"] == "name":
                return self._get_site_name(resource)

            if str(resource.graph_id) == "df3ee1ae-9c1c-11ec-964d-5254008afee6" and config["type"] == "map_popup":
                formations = self._get_formations(resource)
                if formations:
                    if not return_value:
                        return_value = ""
                    return_value += self._format_value("Formation", formations, config)

            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                nodeid__in=config['node_ids']
            )
            sorted_name_nodes = sorted(name_nodes, key=lambda row: config['node_ids'].index(str(row.nodeid)), reverse=False)

            for name_node in sorted_name_nodes:
                value = self._get_value_from_node(name_node, resource)

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

    def _get_formations(self, resource):
        # print("Resource: %s" % resource.resourceinstanceid)
        if not self._collected_fossils_node:
            self._collected_fossils_node = models.Node.objects.filter(
                alias="fossils_collected"
            ).first()

        if not self._formation_node:
            self._formation_node = models.Node.objects.filter(
                alias='geological_formation',
                graph__name='BC Fossil Sample'
            ).first()

        # if not self._geologic_period_node:
        #     self._formation_node = models.Node.objects.filter(
        #         alias='period',
        #         graph__name='BC Fossil Sample'
        #     ).first()

        fossil_sample_values = models.ResourceXResource.objects.filter(
            resourceinstanceidfrom=resource.resourceinstanceid,
            nodeid=self._collected_fossils_node.nodeid
        ).values_list('resourceinstanceidto', flat=True)

        tiles = models.TileModel.objects.filter(
            nodegroup_id=self._formation_node.nodegroup_id,
            resourceinstance_id__in=fossil_sample_values
        ).all()

        if len(tiles) == 0:
            return None

        datatype = self._get_datatype_factory().get_instance(self._formation_node.datatype)

        formations = []
        for tile in tiles:
            formation_value = datatype.get_display_value(tile, self._formation_node)
            if formation_value:
                formations.append(formation_value)

        if len(formations) > 0:
            return ', '.join(list(set(formations)))
        else:
            return None

    def _get_site_name(self, resource):
        display_value = "("

        start_date_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Collection Start Year") .first()
        end_date_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Collection End Year") .first()
        geographical_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Geographical Name") .first()

        if start_date_node:
            value = self._get_value_from_node(
                start_date_node, resource.resourceinstanceid
            )
        else:
            value = "?"
        display_value += value if value else "?"

        if end_date_node:
            value = self._get_value_from_node(
                end_date_node, resource.resourceinstanceid
            )
        else:
            value = "?"
        display_value += (", " + value) if value else ""
        display_value += ") - "

        if geographical_node:
            value = self._get_value_from_node(
                geographical_node, resource.resourceinstanceid
            )
        else:
            value = "Unknown"
        display_value += value if value else "?"

        return display_value

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value

    def _nodeid_to_sequence(self, id_list, row):
        return id_list.index(row.nodeid)
