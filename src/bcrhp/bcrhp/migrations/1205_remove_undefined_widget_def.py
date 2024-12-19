from django.db import migrations
from arches.app.models import models


def unregister_widget(self, name):
    """
    Removes a function from the system

    """
    try:
        instances = models.Widget.objects.filter(name="bchp-map-widget")
        instances[0].delete()
    except Exception as e:
        print(e)


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1081_add_missing_featureids")]

    operations = [
        migrations.RunPython(unregister_widget, migrations.RunPython.noop),
    ]
