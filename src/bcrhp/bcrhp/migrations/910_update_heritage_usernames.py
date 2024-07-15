from django.db import migrations
from django.contrib.auth import get_user_model

users_to_update = ["emjohnst", "kmcevoy", "bferguso"]


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "636_update_search_card_descriptor"),
    ]

    def add_suffix(apps, schema_editor, with_create_permissions=True):

        for username in users_to_update:
            if get_user_model().objects.filter(username=username).exists() and not get_user_model().objects.filter(username=username + "@idir").exists():
                user = get_user_model().objects.get(username=username)
                user.username = username + "@idir"
                user.save()

    def remove_suffix(apps, schema_editor, with_create_permissions=True):

        for username in users_to_update:
            if get_user_model().objects.filter(username=username+"@idir").exists() and not get_user_model().objects.filter(username=username).exists():
                user = get_user_model().objects.get(username=username + "@idir")
                user.username = user.username.replace("@idir", "")
                user.save()

    operations = [
        migrations.RunPython(add_suffix, remove_suffix),
    ]

