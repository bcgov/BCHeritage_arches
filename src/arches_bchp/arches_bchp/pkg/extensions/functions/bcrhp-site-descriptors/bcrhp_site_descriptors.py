from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from django.utils.translation import ugettext as _
from arches_bchp.util.bcrhp_aliases import BCRHPSiteAliases as aliases

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
    # For Name part of descriptor
    en_graph = {"en": "BC Heritage Resource"}

    _empty_name_value = '(No official name)'
    _nodes = {}
    _datatypes = {}

    _initialized = False

    # @todo Change these to aliases
    _popup_order = ['Borden Number', 'Address', 'Recognition Type']
    _popup_order2 = [aliases.BORDEN_NUMBER, 'address', aliases.RECOGNITION_TYPE]
    _card_order = ['Borden Number', 'City', 'Recognition Type', 'Construction Date']
    _card_order2 = [aliases.BORDEN_NUMBER, aliases.CITY, aliases.RECOGNITION_TYPE, 'construction_date']
    _address_order = [['Street Number', 'Street Name'],['City','Postal Code']]
    _address_order2 = [['street_number', 'street_name'],['city','postal_code']]


    # Initializes the static nodes and datatypes data
    def initialize(self):
        for alias in [aliases.NAME_TYPE, aliases.NAME, aliases.START_YEAR, aliases.START_YEAR_QUALIFIER, aliases.SIGNIFICANT_EVENTS]:
            BCRHPSiteDescriptors._nodes[alias] = models.Node.objects.filter(
                alias=alias,
                graph__name__contains=BCRHPSiteDescriptors.en_graph
            ).first()
            BCRHPSiteDescriptors._datatypes[alias] = BCRHPSiteDescriptors._datatype_factory.get_instance(BCRHPSiteDescriptors._nodes[alias].datatype)

        BCRHPSiteDescriptors._initialized = True

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        if not BCRHPSiteDescriptors._initialized:
            self.initialize()

        return_value = ""

        display_values = {}

        try:
            if config["type"] == "name":
                return self._get_site_name(resource)

            _description_order = self._popup_order if config["type"] == 'map_popup' else self._card_order

            all_names = _description_order+[item for sublist in (self._address_order) for item in sublist]
            name_nodes = models.Node.objects.filter(graph=resource.graph_id).filter(
                name__in=all_names
            )

            sorted_name_nodes = sorted(name_nodes, key=lambda row: _description_order.index(row.name) if row.name in _description_order else 999, reverse=False)

            for name_node in sorted_name_nodes:
                value = self._get_value_from_node(name_node, resource)
                if value:
                    if config["first_only"]:
                        return BCRHPSiteDescriptors._format_value(name_node.name, value, config)
                    display_values[name_node.name] = value

            for label in _description_order:
                if label == 'Address':
                    return_value += BCRHPSiteDescriptors._format_value(label, BCRHPSiteDescriptors._get_address(display_values), config)
                elif label == 'Construction Date':
                    return_value += BCRHPSiteDescriptors._format_value(label, BCRHPSiteDescriptors._get_construction_date(resource), config)
                elif label in display_values:
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
        if value is None:
            return ""
        elif config["show_name"]:
            return "<div class='bc-popup-entry'><div class='bc-popup-label'>%s</div><div class='bc-popup-value'>%s</div></div>" % (name, value)
        return value

    @staticmethod
    def _get_address(display_values):
        address = ""
        for label_line in BCRHPSiteDescriptors._address_order:
            if address:
                address += "<br>"
            line = ""
            for label in label_line:
                if label in display_values:
                    if (line):
                        line += " "
                    line += display_values[label] if display_values[label] else ""
            if line:
                address += line
        return address if address else None

    @staticmethod
    def _get_construction_date(resource):

        tiles = models.TileModel.objects.filter(
            nodegroup_id=BCRHPSiteDescriptors._nodes[aliases.START_YEAR].nodegroup_id
        ).filter(resourceinstance_id=resource)
        if not tiles:
            return None
        nodes = BCRHPSiteDescriptors._nodes
        data_types = BCRHPSiteDescriptors._datatypes
        for tile in tiles:
            if data_types[aliases.SIGNIFICANT_EVENTS].get_display_value(tile, nodes[aliases.SIGNIFICANT_EVENTS]) == 'Construction':
                qualifier = data_types[aliases.START_YEAR_QUALIFIER].get_display_value(tile, nodes[aliases.START_YEAR_QUALIFIER])
                const_date = data_types[aliases.START_YEAR].get_display_value(tile, nodes[aliases.START_YEAR])
                if const_date:
                    return ("{qualifier} {const_date}" if qualifier else "{const_date}").format(qualifier=qualifier, const_date=const_date)
        return None

    def _get_site_name(self, resource):
        name_datatype = BCRHPSiteDescriptors._datatypes[aliases.NAME]
        name_type_datatype = BCRHPSiteDescriptors._datatypes[aliases.NAME_TYPE]
        display_value = ''

        for tile in models.TileModel.objects.filter(
                nodegroup_id=BCRHPSiteDescriptors._nodes[aliases.NAME].nodegroup_id
        ).filter(resourceinstance_id=resource.resourceinstanceid).all():
            if name_type_datatype.get_display_value(tile, BCRHPSiteDescriptors._nodes[aliases.NAME_TYPE]) == 'Primary':
                name = name_datatype.get_display_value(tile, BCRHPSiteDescriptors._nodes[aliases.NAME])
                if display_value and name:
                    display_value = display_value + ",<br>"
                if name:
                    display_value = display_value + name

        return display_value if display_value else self._empty_name_value
