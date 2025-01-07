from django.db import migrations
from django.core.management import call_command
from bcgov_arches_common.util.pkg_util import (
    get_mapbox_spec_files as get_common_mapbox_spec_files,
    update_map_source_prefix,
)
from bcfms.util.pkg_util import get_mapbox_spec_files


def reload_map_layers(apps, schema_editor):
    # Common map layers
    for layer_spec in get_common_mapbox_spec_files():
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


def update_prefixes(apps, schema_editor):
    update_map_source_prefix("bc-fossil-management")


reset_layer_sql = """
    update map_layers a set addtomap = addtomap_updated
        from (select maplayerid, name, case when name ~ '^Parks' or name = 'British Columbia Roads' then true else false end addtomap_updated, addtomap
        from map_layers) b
        where a.maplayerid = b.maplayerid;
        """


class Migration(migrations.Migration):
    dependencies = [("bcfms", "1125_update_mapdata_query")]

    operations = [
        migrations.RunPython(reload_map_layers, migrations.RunPython.noop),
        migrations.RunSQL(reset_layer_sql, migrations.RunSQL.noop),
        migrations.RunPython(update_prefixes, migrations.RunPython.noop),
    ]
