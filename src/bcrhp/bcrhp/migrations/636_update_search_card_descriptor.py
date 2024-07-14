from django.db import migrations
from arches.app.models.graph import Graph
from django.core.management import call_command


def reindex_heritage_sites(apps, schema_editor, with_create_permissions=True):
    slugs = ["heritage_site"]

    graphs = Graph.objects.filter(slug__in=slugs).all()

    print(
        "Recalculating resource descriptors in graphs: %s"
        % [graph.slug for graph in graphs]
    )
    call_command(
        "es",
        "index_resources_by_type",
        resource_types=[graph.graphid for graph in graphs],
        recalculate_descriptors=True,
    )


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "992_add_resource_exporter_to_anonymous"),
    ]

    operations = [
        migrations.RunPython(reindex_heritage_sites, migrations.RunPython.noop),
    ]
