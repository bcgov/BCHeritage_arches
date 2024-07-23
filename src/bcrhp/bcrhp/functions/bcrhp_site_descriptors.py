from arches.app.functions.primary_descriptors import AbstractPrimaryDescriptorsFunction
from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from bcrhp.util.bcrhp_aliases import BCRHPSiteAliases as aliases

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
            },
        },
        "triggering_nodegroups": [],
    },
    "classname": "BCRHPSiteDescriptors",
    "component": "views/components/functions/bcrhp-site-descriptors",
}


class BCRHPSiteDescriptors(AbstractPrimaryDescriptorsFunction):
    _datatype_factory = DataTypeFactory()
    # For Name part of descriptor
    en_graph = {"en": "Heritage Site"}

    _empty_name_value = "(No official name)"
    _nodes = {}
    _datatypes = {}

    _initialized = False

    # @todo Change these to aliases
    _name_nodes = [aliases.NAME_TYPE, aliases.NAME, aliases.BORDEN_NUMBER]
    _sig_event_nodes = [
        aliases.START_YEAR,
        aliases.DATES_APPROXIMATE,
        aliases.CHRONOLOGY,
    ]
    _popup_nodes = [aliases.CITY, "address"]
    _card_nodes = [aliases.CITY, "construction_date", aliases.REGISTRATION_STATUS]
    _address_nodes = [["street_address"], [aliases.CITY, "postal_code"]]

    # Initializes the static nodes and datatypes data
    def initialize(self):
        for alias in (
            BCRHPSiteDescriptors._name_nodes
            + BCRHPSiteDescriptors._sig_event_nodes
            + BCRHPSiteDescriptors._popup_nodes
            + BCRHPSiteDescriptors._card_nodes
            + sum(BCRHPSiteDescriptors._address_nodes, [])
        ):
            node = models.Node.objects.filter(
                alias=alias, graph__name__contains=BCRHPSiteDescriptors.en_graph
            ).first()
            if node:
                BCRHPSiteDescriptors._nodes[alias] = node
                BCRHPSiteDescriptors._datatypes[alias] = (
                    BCRHPSiteDescriptors._datatype_factory.get_instance(node.datatype)
                )

        BCRHPSiteDescriptors._initialized = True

    def get_primary_descriptor_from_nodes(
        self, resource, config, context=None, descriptor=None
    ):
        if not BCRHPSiteDescriptors._initialized:
            self.initialize()

        return_value = ""
        display_values = {}

        try:
            if config["type"] == "name":
                return self._get_site_name(resource)

            _description_order = (
                self._popup_nodes if config["type"] == "map_popup" else self._card_nodes
            )

            nodes = BCRHPSiteDescriptors._nodes

            for node_alias in _description_order:
                value = BCRHPSiteDescriptors._get_value_from_node(node_alias, resource)
                if value:
                    if config["first_only"]:
                        return BCRHPSiteDescriptors._format_value(
                            nodes[node_alias].name, value, config
                        )
                    display_values[node_alias] = value

            for alias in _description_order:
                if alias == "address":
                    return_value += BCRHPSiteDescriptors._format_value(
                        "Address", BCRHPSiteDescriptors._get_address(resource), config
                    )
                elif alias == "construction_date":
                    return_value += BCRHPSiteDescriptors._format_value(
                        "Construction Date",
                        BCRHPSiteDescriptors._get_construction_date(resource),
                        config,
                    )
                elif alias in display_values:
                    return_value += BCRHPSiteDescriptors._format_value(
                        nodes[alias].name, display_values[alias], config
                    )

            return return_value

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    @staticmethod
    def _get_value_from_node(node_alias, resourceinstanceid=None, data_tile=None):
        """
        get the display value from the resource tile(s) for the node with the given name

        Keyword Arguments

        node_alias -- node alias of the data to extract
        resourceinstanceid -- id of resource instance used to fetch the tile(s) if data_tile not specified
        data_tile -- if specified, the tile to extract the value from
        """
        if node_alias not in BCRHPSiteDescriptors._nodes:
            return None

        display_values = []
        datatype = BCRHPSiteDescriptors._datatypes[node_alias]

        tiles = (
            [data_tile]
            if data_tile
            else models.TileModel.objects.filter(
                nodegroup_id=BCRHPSiteDescriptors._nodes[node_alias].nodegroup_id
            ).filter(resourceinstance_id=resourceinstanceid)
        )

        for tile in tiles:
            if tile:
                display_values.append(
                    datatype.get_display_value(
                        tile, BCRHPSiteDescriptors._nodes[node_alias]
                    )
                )

        return (
            None
            if len(display_values) == 0
            else (display_values[0] if len(display_values) == 1 else display_values)
        )

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
            return (
                "<div class='bc-popup-entry'><div class='bc-popup-label'>%s</div><div class='bc-popup-value'>%s</div></div>"
                % (name, value)
            )
        return value

    @staticmethod
    def _get_address(resource):
        address = ""
        nodes = BCRHPSiteDescriptors._nodes

        for address_line_nodes in BCRHPSiteDescriptors._address_nodes:
            if address:
                address += "<br>"
            line = ""
            for address_node_alias in address_line_nodes:
                tile = (
                    models.TileModel.objects.filter(
                        nodegroup_id=nodes[address_node_alias].nodegroup_id
                    )
                    .filter(resourceinstance_id=resource.resourceinstanceid)
                    .first()
                )
                if line:
                    line += " "
                display_value = BCRHPSiteDescriptors._get_value_from_node(
                    node_alias=address_node_alias, data_tile=tile
                )
                display_value = (
                    display_value[0] if type(display_value) is list else display_value
                )
                line += display_value if display_value is not None else ""
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
            if (
                data_types[aliases.CHRONOLOGY].get_display_value(
                    tile, nodes[aliases.CHRONOLOGY]
                )
                == "Construction"
            ):
                qualifier = (
                    "Circa"
                    if data_types[aliases.DATES_APPROXIMATE].get_display_value(
                        tile, nodes[aliases.DATES_APPROXIMATE]
                    )
                    == "True"
                    else ""
                )
                const_date = data_types[aliases.START_YEAR].get_display_value(
                    tile, nodes[aliases.START_YEAR]
                )
                if const_date:
                    return (
                        "{qualifier} {const_date}" if qualifier else "{const_date}"
                    ).format(qualifier=qualifier, const_date=const_date)
        return None

    def _get_site_name(self, resource):
        name_datatype = BCRHPSiteDescriptors._datatypes[aliases.NAME]
        name_type_datatype = BCRHPSiteDescriptors._datatypes[aliases.NAME_TYPE]
        borden_number_datatype = BCRHPSiteDescriptors._datatypes[aliases.BORDEN_NUMBER]
        display_value = ""

        for tile in (
            models.TileModel.objects.filter(
                nodegroup_id=BCRHPSiteDescriptors._nodes[aliases.NAME].nodegroup_id
            )
            .filter(resourceinstance_id=resource.resourceinstanceid)
            .all()
        ):
            if (
                name_type_datatype.get_display_value(
                    tile, BCRHPSiteDescriptors._nodes[aliases.NAME_TYPE]
                )
                == "Common"
            ):
                name = name_datatype.get_display_value(
                    tile, BCRHPSiteDescriptors._nodes[aliases.NAME]
                )
                if display_value and name:
                    display_value = display_value + ",<br>"
                if name:
                    display_value = display_value + name

        if not display_value:
            display_value = self._empty_name_value

        borden_number_tile = models.TileModel.objects.filter(
            nodegroup_id=BCRHPSiteDescriptors._nodes[
                aliases.BORDEN_NUMBER
            ].nodegroup_id,
            resourceinstance_id=resource.resourceinstanceid,
        ).first()

        if borden_number_tile:
            display_value += " - %s" % borden_number_datatype.get_display_value(
                borden_number_tile, BCRHPSiteDescriptors._nodes[aliases.BORDEN_NUMBER]
            )

        return display_value if display_value else self._empty_name_value
