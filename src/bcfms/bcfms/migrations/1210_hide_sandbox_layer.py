from django.db import migrations


update_sandbox_visbility_sql = """
        update nodes set config = jsonb_set(nodes.config, '{addToMap}', to_jsonb(false))
        where nodes.nodeid = (
        select nodeid from nodes
                 join graphs g on nodes.graphid = g.graphid
                 where datatype = 'geojson-feature-collection'
        and g.slug = 'project_sandbox');
"""

revert_sandbox_visbility_sql = """
        update nodes set config = jsonb_set(nodes.config, '{addToMap}', to_jsonb(true))
        where nodes.nodeid = (
        select nodeid from nodes
                 join graphs g on nodes.graphid = g.graphid
                 where datatype = 'geojson-feature-collection'
        and g.slug = 'project_sandbox');
"""


class Migration(migrations.Migration):
    dependencies = [("bcfms", "1203_update_resource_model_legends")]

    operations = [
        migrations.RunSQL(update_sandbox_visbility_sql, revert_sandbox_visbility_sql),
    ]
