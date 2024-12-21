from django.db import migrations
from django.core.management import call_command
from bcrhp.util.pkg_util import get_mapbox_spec_files


def reload_map_layers(apps, schema_editor):
    # BCFMS-specific map layers
    for layer_spec in get_mapbox_spec_files():
        call_command(
            "packages",
            operation="delete_mapbox_layer",
            layer_name=layer_spec["name"],
        )
        call_command(
            "packages",
            operation="add_mapbox_layer",
            layer_name=layer_spec["name"],
            mapbox_json_path=layer_spec["path"],
        )


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1205_remove_undefined_widget_def")]

    operations = [
        migrations.RunPython(reload_map_layers, migrations.RunPython.noop),
    ]