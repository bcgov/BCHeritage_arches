from django.db import migrations

disable_emails = """
    update notification_types set emailnotify = false
        where typeid = '441e6ed4-188d-11ea-a35b-784f435179ea';
    update user_x_notification_types nt
        set emailnotify = false
        where notiftype_id = '441e6ed4-188d-11ea-a35b-784f435179ea';
    """

enable_emails = """
    update notification_types set emailnotify = true
        where typeid = '441e6ed4-188d-11ea-a35b-784f435179ea';
    update user_x_notification_types nt
        set emailnotify = true
        where notiftype_id = '441e6ed4-188d-11ea-a35b-784f435179ea';
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "1108_fix_null_card_sortorder"),
    ]

    operations = [
        migrations.RunSQL(disable_emails, enable_emails),
    ]
