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
    _datatype_factory = None
    def get_primary_descriptor_from_nodes(self, resource, config):
        return_value = None
        try:
            # Name for CollectionEvent is a special case
            if str(resource.graph_id) == "df3ee1ae-9c1c-11ec-964d-5254008afee6" and config["type"] == "name":
                return self._get_site_name(resource)

            node_ids = config['node_ids']
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
        if not self._datatype_factory:
            self._datatype_factory = DataTypeFactory()
        datatype = self._datatype_factory.get_instance(name_node.datatype)
        return datatype.get_display_value(tile, name_node)

    def _get_site_name(self, resource):
        display_value = ""
        site = models.ResourceXResource.objects.filter(resourceinstanceidto=resource.resourceinstanceid).prefetch_related("resourceinstancefrom_graphid").first()

        if not site:
            return display_value
        name_node = models.Node.objects.filter(graph=site.resourceinstancefrom_graphid) .filter(name="Site Name") .first()
        start_date_node = models.Node.objects.filter(graph=resource.graph_id) .filter(name="Collection Start Year") .first()
        if start_date_node:
            display_value = self._get_value_from_node(
                start_date_node, resource.resourceinstanceid
            )

        if not display_value:
            display_value = "(?)"

        if name_node:
            display_value = display_value + " - " + self._get_value_from_node(name_node, site.resourceinstanceidfrom)

        return display_value

    def _format_value(self, name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value

    def _nodeid_to_sequence(self, id_list, row):
        return id_list.index(row.nodeid)
