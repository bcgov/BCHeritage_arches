from arches.app.models.graph import Graph
from arches.app.models.models import Group, User
from arches.app.models.resource import Resource
import logging
from .business_data_proxy import HeritageSiteDataProxy
from guardian.shortcuts import (
    assign_perm,
    get_perms,
    remove_perm,
    get_users_with_perms,
    get_groups_with_perms,
)


logger = logging.getLogger(__name__)


class AdminOnlyPermissionManager:
    admin_only_graph_slugs = [
        "lg_person",
        "site_submission",
        "project_sandbox",
        "heritage_site_historical_data",
    ]
    restricted_usernames = ["anonymous"]
    restricted_group_names = ["Guest"]
    no_access_perm = "no_access_to_resourceinstance"
    restricted_users = None
    restricted_groups = None

    def __init__(self):
        self._populate_restricted_objects()

    def _populate_restricted_objects(self):
        self.restricted_groups = list(
            Group.objects.filter(name__in=self.restricted_group_names).all()
        )
        self.restricted_users = list(
            User.objects.filter(username__in=self.restricted_usernames).all()
        )

    def _is_resource_restricted(self, obj):
        return True

    def _get_resource_instances(self, slug):
        graph = Graph.objects.get(slug=slug)
        return Resource.objects.filter(graph=graph).all()

    def reset_all_permissions(self, graph_slugs=None, clear_all_permissions=False):
        processed_graphs = []
        slugs_to_process = (
            self.admin_only_graph_slugs
            if not graph_slugs
            else (graph_slugs if type(graph_slugs) is list else [graph_slugs])
        )
        for slug in slugs_to_process:
            if slug in self.admin_only_graph_slugs:
                print("Processing: %s " % slug, end="", flush=True)
                processed_graphs.append(slug)
                resources = self._get_resource_instances(slug)

                for idx, obj in enumerate(resources):
                    if clear_all_permissions:
                        self.remove_all_object_permissions(obj)
                    self.apply_object_permissions(obj)

                    if (idx % 100) == 0:
                        print(".", end="", flush=True)
                print("\nProcessed %s %s" % (len(resources), slug))
        return processed_graphs

    def apply_object_permissions(self, obj):
        for user_or_group in self.restricted_users + self.restricted_groups:
            if self._is_resource_restricted(obj):
                assign_perm(
                    perm=self.no_access_perm, user_or_group=user_or_group, obj=obj
                )
            else:
                remove_perm(
                    perm=self.no_access_perm, user_or_group=user_or_group, obj=obj
                )

    def remove_object_permissions(self, permission, obj, user_or_group=None):
        for entity in (
            get_users_with_perms(obj) + get_groups_with_perms(obj)
            if user_or_group is None
            else [user_or_group]
        ):
            remove_perm(user_or_group=entity, obj=obj, perm=permission)

    def remove_all_object_permissions(self, obj, user_or_group=None):
        for entity in (
            list(get_users_with_perms(obj)) + list(get_groups_with_perms(obj))
            if user_or_group is None
            else [user_or_group]
        ):
            for perm in get_perms(user_or_group=entity, obj=obj):
                remove_perm(user_or_group=entity, obj=obj, perm=perm)


class HeritageSitePermissionManager(AdminOnlyPermissionManager):

    def __init__(self):
        super().__init__()
        self.admin_only_graph_slugs = ["heritage_site"]
        self._populate_restricted_objects()

    def _is_resource_restricted(self, obj):
        return not HeritageSiteDataProxy().is_site_public(obj)
