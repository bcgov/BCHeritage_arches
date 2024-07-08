from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from guardian.shortcuts import get_perms, assign_perm, remove_perm
from django.core.management import call_command


def add_permissions(apps, schema_editor, with_create_permissions=True):
    slugs = ["lg_person", "site_submission", "project_sandbox"]

    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()
    print("Guest group: %s" % guest_group)
    graphs = Graph.objects.filter(slug__in=slugs).all()

    resources = Resource.objects.filter(graph__slug__in=slugs).all()
    print(len(resources))
    for resource in resources:
        print(
            "Resource: %s, %s"
            % (resource.get_descriptor("name", {}), resource.graph.slug)
        )
        print(
            "User: %s, group: %s "
            % (get_perms(user, resource), get_perms(guest_group, resource))
        )
        assign_perm("no_access_to_resourceinstance", user, obj=resource)
        assign_perm("no_access_to_resourceinstance", guest_group, obj=resource)
        print(
            "User: %s, group: %s "
            % (get_perms(user, resource), get_perms(guest_group, resource))
        )
        print(get_perms(user, resource))

    print("Reindexing resources in graphs: %s" % [graph.slug for graph in graphs])
    call_command(
        "es",
        "index_resources_by_type",
        resource_types=[graph.graphid for graph in graphs],
    )


def remove_permissions(apps, schema_editor, with_create_permissions=True):
    slugs = ["lg_person", "site_submission", "project_sandbox"]
    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()

    graphs = Graph.objects.filter(slug__in=slugs).all()
    resources = Resource.objects.filter(graph__slug__in=slugs).all()

    print(len(resources))
    for resource in resources:
        print(
            "Resource: %s, %s"
            % (resource.get_descriptor("name", {}), resource.graph.slug)
        )
        print(
            "User: %s, group: %s "
            % (get_perms(user, resource), get_perms(guest_group, resource))
        )
        remove_perm("no_access_to_resourceinstance", user, obj=resource)
        remove_perm("no_access_to_resourceinstance", guest_group, obj=resource)
        print(get_perms(user, resource))

    print("Reindexing resources in graphs: %s" % [graph.slug for graph in graphs])
    call_command(
        "es",
        "index_resources_by_type",
        resource_types=[graph.graphid for graph in graphs],
    )

    private_resources_sql = """
    select distinct resourceinstanceid from heritage_site.site_record_admin
         where restricted=true
                or __arches_get_concept_label(bcrhp_submission_status) not in ('Approved - Basic Record', 'Approved - Full Record')
union
select resourceinstanceid from heritage_site.bc_right where not officially_recognized_site
or __arches_get_concept_label(registration_status) not in ('Registered','Federal Jurisdiction');
"""
    # db_alias = schema_editor.connection.alias
    # Group = apps.get_model("auth", "Group")
    # Permission = apps.get_model("auth", "Permission")
    #
    # write_nodegroup = Permission.objects.get(codename='write_nodegroup', content_type__app_label='models', content_type__model='nodegroup')
    # delete_nodegroup = Permission.objects.get(codename='delete_nodegroup', content_type__app_label='models', content_type__model='nodegroup')
    #
    # resource_editor_group = Group.objects.using(db_alias).get(name='Resource Editor')
    # resource_editor_group.permissions.remove(write_nodegroup)
    # resource_editor_group.permissions.remove(delete_nodegroup)
    # resource_editor_group = Group.objects.using(db_alias).get(name='Resource Reviewer')
    # resource_editor_group.permissions.remove(write_nodegroup)
    # resource_editor_group.permissions.remove(delete_nodegroup)
    # resource_editor_group = Group.objects.using(db_alias).get(name='Crowdsource Editor')
    # resource_editor_group.permissions.remove(write_nodegroup)
    # resource_editor_group.permissions.remove(delete_nodegroup)


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "893_apply_admin_only_function"),
    ]

    operations = [
        ## the following command has to be run after the previous RunSQL commands that update the domain datatype values
        migrations.RunPython(add_permissions, remove_permissions),
    ]

