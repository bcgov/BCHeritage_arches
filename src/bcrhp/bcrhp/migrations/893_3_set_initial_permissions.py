from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.resource import Resource
from arches.app.models.graph import Graph
from guardian.shortcuts import assign_perm, remove_perm
from django.core.management import call_command

slugs = [
    "lg_person",
    "site_submission",
    "project_sandbox",
    "heritage_site_historical_data",
]


def add_permissions(apps, schema_editor, with_create_permissions=True):

    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()
    graphs = Graph.objects.filter(slug__in=slugs).all()

    resources = Resource.objects.filter(graph__slug__in=slugs).all()
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
    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()

    graphs = Graph.objects.filter(slug__in=slugs).all()
    resources = Resource.objects.filter(graph__slug__in=slugs).all()

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
        ("bcrhp", "893_2_apply_admin_only_function"),
    ]

    operations = [
        migrations.RunPython(add_permissions, remove_permissions),
    ]
