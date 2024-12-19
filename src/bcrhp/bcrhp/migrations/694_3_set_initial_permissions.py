from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from guardian.shortcuts import assign_perm, remove_perm
from django.core.management import call_command

private_resources_sql = """
    select distinct resourceinstanceid from heritage_site.site_record_admin
         where restricted=true
                or __arches_get_concept_label(bcrhp_submission_status) not in ('Approved - Basic Record', 'Approved - Full Record')
    union
    select resourceinstanceid from heritage_site.bc_right 
        where not officially_recognized_site
        or __arches_get_concept_label(registration_status) not in ('Registered','Federal Jurisdiction')
    union
    (select resourceinstanceid from heritage_site.instances i except (
        select resourceinstanceid from heritage_site.bc_right r));
"""


def add_permissions(apps, schema_editor, with_create_permissions=True):
    slugs = ["heritage_site"]

    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()
    graphs = Graph.objects.filter(slug__in=slugs).all()

    resources = Resource.objects.raw(private_resources_sql)
    print(len(resources))
    for resource in resources:
        assign_perm("no_access_to_resourceinstance", user, obj=resource)
        assign_perm("no_access_to_resourceinstance", guest_group, obj=resource)

    print("Reindexing resources in graphs: %s" % [graph.slug for graph in graphs])
    call_command(
        "es",
        "index_resources_by_type",
        resource_types=[graph.graphid for graph in graphs],
    )


def remove_permissions(apps, schema_editor, with_create_permissions=True):
    slugs = ["heritage_site"]
    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()

    graphs = Graph.objects.filter(slug__in=slugs).all()
    resources = Resource.objects.raw(private_resources_sql)

    print(len(resources))
    for resource in resources:
        remove_perm("no_access_to_resourceinstance", user, obj=resource)
        remove_perm("no_access_to_resourceinstance", guest_group, obj=resource)

    print("Reindexing resources in graphs: %s" % [graph.slug for graph in graphs])
    call_command(
        "es",
        "index_resources_by_type",
        resource_types=[graph.graphid for graph in graphs],
    )


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "694_2_apply_restricted_site_access_function"),
    ]

    operations = [
        migrations.RunPython(add_permissions, remove_permissions),
    ]
