from arches.app.models import models
from arches_bchp.util.bcrhp_aliases import BCRHPSiteAliases as site_aliases, BCRHPOrgAliases as aliases
from arches_bchp.functions.base.bc_resource_descriptors import BCResourceDescriptors

details = {
    "functionid": "60000000-0000-0000-0000-000000001003",
    "name": "BCRHP Organization Descriptors",
    "type": "primarydescriptors",
    "modulename": "bcrhp_org_descriptors.py",
    "description": "Function that provides the primary descriptors for BCRHP Organization Resources",
    "defaultconfig": {
        "module": "arches_bcrhp.functions.bcrhp_org_descriptors",
        "class_name": "BCRHPOrgDescriptors",
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
    "classname": "BCRHPOrgDescriptors",
    "component": "views/components/functions/bcrhp-org-descriptors",
}


class BCRHPOrgDescriptors(BCResourceDescriptors):
    _graph_name = "BC Local Government"
    _site_graph_name = "BC Heritage Resource"

    _responsible_gov_node = None

    _name_nodes = [aliases.NAME]
    _popup_nodes = [aliases.GOVERNMENT_TYPE]
    _card_nodes = [aliases.GOVERNMENT_TYPE]

    def __init__(self):
        super(BCResourceDescriptors, self).__init__()
        super().en_graph["en"] = BCRHPOrgDescriptors._graph_name
        BCRHPOrgDescriptors._responsible_gov_node = models.Node.objects.filter(
            alias=site_aliases.RESPONSIBLE_GOVERNMENT,
            graph__name__contains={"en": BCRHPOrgDescriptors._site_graph_name}
        ).first()

    def get_primary_descriptor_from_nodes(self, resource, config, context=None):
        if not BCRHPOrgDescriptors._initialized:
            super().initialize(BCRHPOrgDescriptors._name_nodes + BCRHPOrgDescriptors._popup_nodes + BCRHPOrgDescriptors._card_nodes)

        return_value = ""

        try:
            if config["type"] == "name":
                return super()._get_value_from_node(aliases.NAME, resource)

            value = super()._get_value_from_node(aliases.GOVERNMENT_TYPE, resource)
            if value:
                return_value += super()._format_value("Type", value, config)
            value = self._get_site_count(resource)
            return_value += super()._format_value("Sites", value, config)
            return return_value

        except ValueError as e:
            print(e, "invalid nodegroupid participating in descriptor function.")

    def _get_site_count(self, resource):
        return models.ResourceXResource.objects.filter(
            resourceinstanceidto=resource
        ).filter(
            nodeid=self._responsible_gov_node.nodeid
        ).count()

    #     return display_value if display_value else self._empty_name_value
