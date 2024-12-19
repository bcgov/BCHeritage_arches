from django.db import migrations
import os
from .util.migration_util import format_files_into_sql


class Migration(migrations.Migration):
    dependencies = [("bcfms", "1120_add_missing_featureids")]

    sql_dir = os.path.join(os.path.dirname(__file__), "sql")
    update_map_attribute_data_function = format_files_into_sql(
        ["2024-12-02_get_map_attribute_data.sql"], sql_dir
    )
    revert_map_attribute_data_function = format_files_into_sql(
        ["2024-05-15_get_map_attribute_data.sql"], sql_dir
    )

    operations = [
        migrations.RunSQL(
            update_map_attribute_data_function, revert_map_attribute_data_function
        )
    ]
