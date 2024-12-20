from django.db import migrations


update_legend_sql = """
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                          '"<p><div class=\\"important-fossil-area legend-swatch\\"></div>Area Boundary</p>"'
                              ::jsonb)
        where graphid = '4d6c9226-10c6-11ec-9a94-5254008afee6' and alias = 'area_boundary'; -- Important Fossil Area
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                    '"<p><div class=\\"provincially-protected-site legend-swatch\\"></div>Area Boundary</p>"'
                              ::jsonb)
        where graphid = 'dd19a93a-0202-11ed-a511-0050568377a0' and alias = 'area_boundary'; -- Provincially Protected Fossil Site
"""

revert_legend_sql = """
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                          '"<p><img alt=\\"\\" class=\\"important-fossil-area legend-swatch\\" src=\\"/bc-fossil-management/static/img/blank.png\\" />Area Boundary</p>"'
                              ::jsonb)
        where graphid = '4d6c9226-10c6-11ec-9a94-5254008afee6' and alias = 'area_boundary'; -- Important Fossil Area
        update nodes
        set config =
                jsonb_set(config, '{layerLegend}',
                          '"<p><img alt=\\"\\" class=\\"provincially-protected-site legend-swatch\\" src=\\"/bc-fossil-management/static/img/blank.png\\" />Area Boundary</p>"'
                              ::jsonb)
        where graphid = 'dd19a93a-0202-11ed-a511-0050568377a0' and alias = 'area_boundary'; -- Provincially Protected Fossil Site
"""


class Migration(migrations.Migration):
    dependencies = [("bcfms", "1203_reload_map_layers")]

    operations = [
        migrations.RunSQL(update_legend_sql, revert_legend_sql),
    ]
