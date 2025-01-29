from django.db import migrations
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from arches.app.models.graph import Graph
from arches.app.models.models import Node
from guardian.shortcuts import assign_perm, remove_perm

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


def add_permissions(apps, schema_editor, with_create_permissions=True):

    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()

    for nodegroup in get_nodegroups():
        print("Nodegroup: %s" % nodegroup)
        assign_perm("no_access_to_nodegroup", user, obj=nodegroup)
        assign_perm("no_access_to_nodegroup", guest_group, obj=nodegroup)


def remove_permissions(apps, schema_editor, with_create_permissions=True):

    user = get_user_model().objects.get(username="anonymous")
    guest_group = Group.objects.filter(name="Guest").first()

    for nodegroup in get_nodegroups():
        remove_perm("no_access_to_nodegroup", user, obj=nodegroup)
        remove_perm("no_access_to_nodegroup", guest_group, obj=nodegroup)


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "893_3_set_initial_permissions"),
    ]

    operations = [
        migrations.RunPython(add_permissions, remove_permissions),
    ]
