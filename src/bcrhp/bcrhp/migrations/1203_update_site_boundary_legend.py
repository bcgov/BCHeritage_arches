from django.db import migrations


update_legend_sql = """
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                          '"<p><div class=\\"legend-swatch site-provincial\\"></div>Provincial<br />\\n<div class=\\"legend-swatch site-federal\\"></div>Federal<br/>\\n<div class=\\"legend-swatch site-municipal\\"></div>Municipal</p>\\n"'::jsonb)
        where alias = 'site_boundary';
"""

revert_legend_sql = """
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                          '"<p><img alt=\\"\\" class=\\"legend-swatch site-provincial\\" src=\\"/int/bc-fossil-management/static/img/blank.png\\" />Provincial<br />\\n<img alt=\\"\\" class=\\"legend-swatch site-federal\\" src=\\"/int/bc-fossil-management/static/img/blank.png\\" />Federal<br />\\n<img alt=\\"\\" class=\\"legend-swatch site-municipal\\" src=\\"/int/bc-fossil-management/static/img/blank.png\\" />Municipal</p>\\n"'::jsonb)
        where alias = 'site_boundary';
"""


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1203_reload_map_layers")]

    operations = [
        migrations.RunSQL(update_legend_sql, revert_legend_sql),
    ]
