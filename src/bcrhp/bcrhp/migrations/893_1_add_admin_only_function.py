from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "893_0_add_historic_data_slug"),
    ]

    sql = """
    insert into functions (functionid, functiontype, name, description, defaultconfig, modulename, classname, component)
    values ('60000000-0000-0000-0000-000000002002',
        'node',
        'Resource Admin Only Access',
        'Disallows all access to non-admin users',
        '{"module": "bcrhp.functions.admin_only_access", "class_name": "AdminOnlyAccess", "triggering_nodegroups": []}',
        'admin_only_access.py',
        'AdminOnlyAccess',
        'views/components/functions/admin-only-access'
    );
    """

    reverse_sql = """
        delete from functions where functionid = '60000000-0000-0000-0000-000000002002';
    """

    operations = [
        migrations.RunSQL(
            sql,
            reverse_sql,
        ),
    ]
