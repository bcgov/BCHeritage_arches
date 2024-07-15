from django.db import migrations
from django.contrib.auth import get_user_model

users_to_update = ["emjohnst", "kmcevoy", "bferguso"]
username_prefix = "idir\\"

class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "636_update_search_card_descriptor"),
    ]

    def add_prefix(apps, schema_editor, with_create_permissions=True):

        for username in users_to_update:
            if get_user_model().objects.filter(username=username).exists() and not get_user_model().objects.filter(username=username_prefix + username).exists():
                user = get_user_model().objects.get(username=username)
                user.username = username_prefix + username
                user.save()

    def remove_prefix(apps, schema_editor, with_create_permissions=True):

        for username in users_to_update:
            if get_user_model().objects.filter(username=username_prefix+username).exists() and not get_user_model().objects.filter(username=username).exists():
                user = get_user_model().objects.get(username=username_prefix+username)
                user.username = user.username.replace(username_prefix, "")
                user.save()

    operations = [
        migrations.RunPython(add_prefix, remove_prefix),
    ]

