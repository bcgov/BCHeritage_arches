from django.db import migrations
import os

class Migration(migrations.Migration):

    reverse_sql_string = ""
    files = [
        '2024-11-29_mv_bc_statement_of_significance.sql',
        '2024-11-29_mv_chronology.sql',
        '2024-11-29_mv_construction_actors.sql',
        '2024-11-29_mv_government.sql',
        '2024-11-29_mv_heritage_class.sql',
        '2024-11-29_mv_heritage_function.sql',
        '2024-11-29_mv_heritage_theme.sql',
        '2024-11-29_mv_property_address.sql',
        '2024-11-29_mv_site_names.sql',
        '2024-11-29_mv_site_protection_event.sql',
        '2024-11-29_mv_site_record_admin.sql',
        '2024-11-29_mv_bc_right.sql',
        '2024-11-29_refresh_materialized_views.sql',
        '2024-11-29_v_historic_site.sql',
        '2024-11-29_v_historic_enviro_onerow_site.sql',
        '2024-11-29_bcrhp_crhp_data_vw.sql'
    ]

    for filename in files:
        file_path = os.path.join(os.path.dirname(__file__), 'sql', filename)
        with open(file_path) as file:
            reverse_sql_string = reverse_sql_string + "\n" + file.read()
    reverse_sql_string = reverse_sql_string + "\n" + " begin; call refresh_materialized_views(); commit;"

    dependencies = [('bcrhp',
                     '1168_fix_mv_chronology_index')]

    drop_materialized_views = """
       drop materialized view if exists mv_bc_statement_of_significance cascade;
       drop materialized view if exists mv_chronology cascade;
       drop materialized view if exists mv_construction_actors cascade;
       drop materialized view if exists mv_government cascade;
       drop materialized view if exists mv_heritage_class cascade;
       drop materialized view if exists mv_heritage_function cascade;
       drop materialized view if exists mv_heritage_theme cascade;
       drop materialized view if exists mv_property_address cascade;
       drop materialized view if exists mv_site_names cascade;
       drop materialized view if exists mv_site_protection_event cascade;
       drop materialized view if exists mv_site_record_admin cascade;
       drop materialized view if exists mv_bc_right cascade;
       drop view if exists bcrhp_crhp_data_vw cascade;
        """

    operations = [
        migrations.RunSQL(drop_materialized_views, reverse_sql_string),
    ]
