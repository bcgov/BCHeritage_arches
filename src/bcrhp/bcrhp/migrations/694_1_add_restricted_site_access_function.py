from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "893_4_restrict_nodes_from_public"),
    ]

    sql = """
    insert into functions (functionid, functiontype, name, description, defaultconfig, modulename, classname, component)
    values ('60000000-0000-0000-0000-000000002003',
        'node',
        'Restricted Site Only Access',
        'Disallows all access to non-admin users',
        '{"module": "bcrhp.functions.restricted_site_access", "class_name": "RestrictedSiteAccess", "triggering_nodegroups": []}',
        'restricted_site_access.py',
        'RestrictedSiteAccess',
        'views/components/functions/restricted-site-access'
    );
    """

    reverse_sql = """
        delete from functions where functionid = '60000000-0000-0000-0000-000000002003';
    """

    operations = [
        migrations.RunSQL(
            sql,
            reverse_sql,
        ),
    ]
