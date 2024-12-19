from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.graph import Graph
from arches.app.models.models import Node

slugs = [
    "lg_person",
    "site_submission",
    "project_sandbox",
    "heritage_site_historical_data",
]


def get_nodegroups():
    graphs = Graph.objects.filter(slug__in=slugs).all()
    nodes = Node.objects.filter(graph__in=graphs)

    site_graph = Graph.objects.filter(slug="heritage_site").first()
    nodegroups = list(set([node.nodegroup for node in nodes]))
    nodegroups.remove(None)
    nodegroups.append(
        Node.objects.filter(graph=site_graph, alias="site_record_admin")
        .first()
        .nodegroup
    )
    nodegroups.append(
        Node.objects.filter(graph=site_graph, alias="internal_remark").first().nodegroup
    )
    print(len(nodegroups))
    return nodegroups


def add_groups(apps, schema_editor, with_create_permissions=True):

    user = get_user_model().objects.get(username="anonymous")
    if not user.groups.filter(name="Guest").exists():
        guest_group = Group.objects.filter(name="Guest").first()
        guest_group.user_set.add(user.id)
        guest_group.save()

    if not user.groups.filter(name="Resource Exporter").exists():
        resource_exporter_group = Group.objects.filter(name="Resource Exporter").first()
        resource_exporter_group.user_set.add(user.id)
        resource_exporter_group.save()


def remove_groups(apps, schema_editor, with_create_permissions=True):

    user = get_user_model().objects.get(username="anonymous")
    if user.groups.filter(name="Resource Exporter").exists():
        resource_exporter_group = Group.objects.filter(name="Resource Exporter").first()
        resource_exporter_group.user_set.remove(user.id)
        resource_exporter_group.save()


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "665_6_correct_public_internal_map_layers"),
    ]

    operations = [
        migrations.RunPython(add_groups, remove_groups),
    ]
