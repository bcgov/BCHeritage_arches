from django.db import migrations
import os
from .util.migration_util import format_files_into_sql
from bcgov_arches_common.migrations.operations.privileged_sql import RunPrivilegedSQL


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1168_fix_mv_chronology_index")]

    files = [
        "2024-11-29_mv_bc_statement_of_significance.sql",
        "2024-11-29_mv_chronology.sql",
        "2024-11-29_mv_construction_actors.sql",
        "2024-11-29_mv_government.sql",
        "2024-11-29_mv_heritage_class.sql",
        "2024-11-29_mv_heritage_function.sql",
        "2024-11-29_mv_heritage_theme.sql",
        "2024-11-29_mv_property_address.sql",
        "2024-11-29_mv_site_names.sql",
        "2024-11-29_mv_site_protection_event.sql",
        "2024-11-29_mv_site_record_admin.sql",
        "2024-11-29_mv_bc_right.sql",
        "2024-11-29_refresh_materialized_views.sql",
        "2024-11-29_v_historic_site.sql",
        "2024-11-29_v_historic_enviro_onerow_site.sql",
        "2024-11-29_bcrhp_crhp_data_vw.sql",
        "2024-11-29_heritage_site.csv_export.sql",
    ]

    sql_dir = os.path.join(os.path.dirname(__file__), "sql")
    create_views = (
        format_files_into_sql(files, sql_dir)
        + "\n"
        + " begin; call refresh_materialized_views(); commit;"
    )

    drop_views = """
       drop view if exists heritage_site.csv_export;
       drop view if exists databc.V_HISTORIC_ENVIRO_ONEROW_SITE;
       drop view if exists bcrhp_crhp_data_vw;
       drop view if exists v_historic_site;
       drop materialized view if exists mv_bc_statement_of_significance;
       drop materialized view if exists mv_chronology;
       drop materialized view if exists mv_construction_actors;
       drop materialized view if exists mv_site_protection_event;
       drop materialized view if exists mv_government;
       drop materialized view if exists mv_heritage_class;
       drop materialized view if exists mv_heritage_function;
       drop materialized view if exists mv_heritage_theme;
       drop materialized view if exists mv_property_address;
       drop materialized view if exists mv_site_names;
       drop materialized view if exists mv_site_record_admin;
       drop materialized view if exists mv_bc_right;
        """

    fix_object_owner_sql = format_files_into_sql(
        files=["2024-12-05_fix_object_owner.sql"], sql_dir=sql_dir
    )

    operations = [
        RunPrivilegedSQL(fix_object_owner_sql, migrations.RunSQL.noop),
        migrations.RunSQL(drop_views, create_views),
    ]
