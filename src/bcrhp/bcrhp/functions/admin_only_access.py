from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm

details = {
    "functionid": "60000000-0000-0000-0000-000000002002",
    "name": "Resource Admin Only Access",
    "type": "node",
    "modulename": "admin_only_access.py",
    "description": "Disallows all access to non-admin users",
    "defaultconfig": {},
    "classname": "AdminOnlyAccess",
    "component": "views/components/functions/admin-only-access",
}


class AdminOnlyAccess(object):
    anonymous_user = None
    guest_group = None

    def __init__(self, config=None, nodegroup_id=None):
        self.config = config
        self.nodegroup_id = nodegroup_id

    def get_guest_group(self):
        if AdminOnlyAccess.guest_group is None:
            AdminOnlyAccess.guest_group = Group.objects.filter(name="Guest").first()
        return AdminOnlyAccess.guest_group

    def get_anonymous_user(self):
        if AdminOnlyAccess.anonymous_user is None:
            AdminOnlyAccess.anonymous_user = get_user_model().objects.get(
                username="anonymous"
            )
        return AdminOnlyAccess.anonymous_user

    def get(self, *args, **kwargs):
        pass

    def save(self, tile, request, context):
        pass

    def post_save(self, tile, request, context):
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
