from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _

details = {
    "functionid": "60000000-0000-0000-0000-000000001002",
    "name": "BCRHP Site Descriptors",
    "type": "primarydescriptors",
    "modulename": "bcrhp_site_descriptors.py",
    "description": "Function that provides the primary descriptors for BC Heritage Resources",
    "defaultconfig": {
        "module": "arches_bcrhp.functions.bcrhp_site_descriptors",
        "class_name": "BCRHPSiteDescriptors",
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
            }
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCRHPSiteDescriptors",
    "component": "views/components/functions/bcrhp-site-descriptors",
}


class BCRHPSiteDescriptors(AbstractPrimaryDescriptorsFunction):
    _datatype_factory = DataTypeFactory()
    _graph_name = 'BC Heritage Resource New'
    # For Name part of descriptor
    _site_name_type_node = models.Node.objects.filter(
        alias='name_type',
        graph__name='BC Heritage Resource New'
    ).first()
    _site_name_node = models.Node.objects.filter(
        alias='name',
        graph__name='BC Heritage Resource New'
    ).first()

    _description_order = ['Borden Number']

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        return_value = None
        display_values = {}

        try:
            if config["type"] == "name":
                return self._get_site_name(resource)

            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                nodeid__in=config['node_ids']
            )
            sorted_name_nodes = sorted(name_nodes, key=lambda row: config['node_ids'].index(str(row.nodeid)), reverse=False)

            for name_node in sorted_name_nodes:
                value = self._get_value_from_node(name_node, resource)
                if value:
                    if config["first_only"]:
                        return BCRHPSiteDescriptors._format_value(name_node.name, value, config)
                    display_values[name_node.name] = value

            for label in BCRHPSiteDescriptors._description_order:
                if label in display_values:
                    if not return_value:
                        return_value = ""
                    else:
                        return_value += config["delimiter"]
                    return_value += BCRHPSiteDescriptors._format_value(label, display_values[label], config)

            return return_value

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_value_from_node(self, name_node, resourceinstanceid):

        tile = models.TileModel.objects.filter(
            nodegroup_id=name_node.nodegroup_id
        ).filter(resourceinstance_id=resourceinstanceid).first()
        if not tile:
            return None
        datatype = BCRHPSiteDescriptors._datatype_factory.get_instance(name_node.datatype)
        return datatype.get_display_value(tile, name_node)

    @staticmethod
    def _format_value(name, value, config):
        if config["show_name"]:
            return "%s: <b>%s</b>" % (name, value)
        return value

    def _get_site_name(self, resource):

        name_datatype = BCRHPSiteDescriptors._datatype_factory.get_instance(BCRHPSiteDescriptors._site_name_node.datatype)
        name_type_datatype = BCRHPSiteDescriptors._datatype_factory.get_instance(BCRHPSiteDescriptors._site_name_type_node.datatype)
        display_value = ''

        for tile in models.TileModel.objects.filter(
            nodegroup_id=BCRHPSiteDescriptors._site_name_node.nodegroup_id
        ).filter(resourceinstance_id=resource.resourceinstanceid).all():
            if name_type_datatype.get_display_value(tile, BCRHPSiteDescriptors._site_name_type_node) == 'Primary':
                if display_value:
                    display_value = display_value + ",<br>"
                display_value = display_value + name_datatype.get_display_value(tile, BCRHPSiteDescriptors._site_name_node)

        return display_value
