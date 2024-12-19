from django.db import migrations

fix_null_sort_order_values = """
    update cards set sortorder = 0 where sortorder is null
                                 and cardid in ('9dc98ec8-5543-45b5-89ce-88edf2618ef7', -- Sandcastle
                                 '1b622c8c-0d0f-11ed-98c2-5254008afee6', -- Heritage Site
                                 '247a4e3c-3122-4351-9b1e-83f1d5e104bb', -- Remaining are Site Submission
                                 '29b8f4ca-7306-406b-9e30-f617e86d3eb5',
                                 '496b9d34-958a-41fd-8302-d6d877bbb477',
                                 '9cb75982-f020-4ac8-9585-0ef3e1589042'
                                 ) 
    """
reverse_fix_null_sort_order_values = """
    update cards set sortorder = 0 where sortorder is null
                                 and cardid in ('9dc98ec8-5543-45b5-89ce-88edf2618ef7', -- Sandcastle
                                 '1b622c8c-0d0f-11ed-98c2-5254008afee6', -- Heritage Site
                                 '247a4e3c-3122-4351-9b1e-83f1d5e104bb', -- Remaining are Site Submission
                                 '29b8f4ca-7306-406b-9e30-f617e86d3eb5',
                                 '496b9d34-958a-41fd-8302-d6d877bbb477',
                                 '9cb75982-f020-4ac8-9585-0ef3e1589042'
                                 ) 
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "1075_fix_null_sortorder"),
    ]

    operations = [
        migrations.RunSQL(
            fix_null_sort_order_values, reverse_fix_null_sort_order_values
        ),
    ]
