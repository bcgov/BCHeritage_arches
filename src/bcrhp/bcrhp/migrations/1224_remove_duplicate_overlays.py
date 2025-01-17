from django.db import migrations
from django.core.management import call_command
from bcrhp.util.pkg_util import get_mapbox_spec_files
from bcgov_arches_common.util.pkg_util import update_map_source_prefix


def reload_map_layers(apps, schema_editor):
    # BCRHP-specific map layers
    call_command(
        "packages",
        operation="delete_mapbox_layer",
        layer_name="Islands Trust Administrative Boundaries Outlined",
    )
    call_command(
        "packages",
        operation="delete_mapbox_layer",
        layer_name="Local Trust Administrative Boundaries",
    )


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1203_update_site_boundary_legend")]

    operations = [
        migrations.RunPython(reload_map_layers, migrations.RunPython.noop),
    ]
