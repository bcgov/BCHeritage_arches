from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "694_1_add_restricted_site_access_function"),
    ]

    sql = """
        with restricted_graphs as (select * from graphs where isresource
                       and slug = 'heritage_site'),
            default_function_config as (select defaultconfig from functions where functionid = '60000000-0000-0000-0000-000000002003')
        insert into functions_x_graphs (id, functionid, graphid, config)
            select uuid_generate_v4(),'60000000-0000-0000-0000-000000002003', graphid, defaultconfig 
            from restricted_graphs, default_function_config;
    """

    reverse_sql = """
        delete from functions_x_graphs where functionid = '60000000-0000-0000-0000-000000002003';
    """

    operations = [
        migrations.RunSQL(
            sql,
            reverse_sql,
        ),
    ]
