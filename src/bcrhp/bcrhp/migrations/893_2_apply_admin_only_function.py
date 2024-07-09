from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "893_1_add_admin_only_function"),
    ]

    sql = """
        with restricted_graphs as (select * from graphs where isresource
                       and slug in ('lg_person', 'site_submission', 'project_sandbox', 'heritage_site_historical_data')),
            default_function_config as (select defaultconfig from functions where functionid = '60000000-0000-0000-0000-000000002002')
        insert into functions_x_graphs (id, functionid, graphid, config)
            select uuid_generate_v4(),'60000000-0000-0000-0000-000000002002', graphid, defaultconfig 
            from restricted_graphs, default_function_config;
    """

    reverse_sql = """
        delete from functions_x_graphs where functionid = '60000000-0000-0000-0000-000000002002';
    """

    operations = [
        migrations.RunSQL(
            sql,
            reverse_sql,
        ),
    ]
