from django.db import migrations

fix_null_sort_order_values = """
    update cards_x_nodes_x_widgets i
        set sortorder =  case when label->>'en' = 'First Name' then 0 else 1 end
       where sortorder is null;
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "1034_fix_file_urls"),
    ]

    operations = [
        migrations.RunSQL(fix_null_sort_order_values, migrations.RunSQL.noop),
    ]
