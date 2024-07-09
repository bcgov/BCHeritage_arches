from guardian.shortcuts import get_perms, assign_perm, remove_perm
from bcrhp.functions.admin_only_access import AdminOnlyAccess
from bcrhp.util.business_data_proxy import HeritageSiteDataProxy

details = {
    "functionid": "60000000-0000-0000-0000-000000002003",
    "name": "Restricted Site Only Access",
    "type": "node",
    "modulename": "restricted_site_access.py",
    "description": "Hides sites that don't meet the public criteria from the anonymous user and Guest group.",
    "defaultconfig": {},
    "classname": "RestrictedSiteAccess",
    "component": "views/components/functions/restricted-site-access",
}


class RestrictedSiteAccess(AdminOnlyAccess):

    def __init__(self, config=None, nodegroup_id=None):
        super().__init__(config, nodegroup_id)

    def get(self, *args, **kwargs):
        pass

    def save(self, tile, request, context):
        pass

    def post_save(self, tile, request, context):
        if HeritageSiteDataProxy().is_site_public(tile.resourceinstance):
            remove_perm(
                "no_access_to_resourceinstance",
                self.get_guest_group(),
                obj=tile.resourceinstance,
            )
            remove_perm(
                "no_access_to_resourceinstance",
                self.get_anonymous_user(),
                obj=tile.resourceinstance,
            )
        else:
            assign_perm(
                "no_access_to_resourceinstance",
                self.get_guest_group(),
                obj=tile.resourceinstance,
            )
            assign_perm(
                "no_access_to_resourceinstance",
                self.get_anonymous_user(),
                obj=tile.resourceinstance,
            )

    def delete(self, tile, request):
        pass

    def on_import(self, *args, **kwargs):
        pass

    # saves changes to the function itself
    def after_function_save(self, *args, **kwargs):
        pass
