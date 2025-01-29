from django.db import migrations

update_config = """
        INSERT INTO cards_x_nodes_x_widgets (cardid, id, config, label, sortorder, nodeid, widgetid, visible)
        VALUES ('9cb75982-f020-4ac8-9585-0ef3e1589042',
                '6504d542-f1d8-4668-bd5b-e46e3e58b617',
                '{
                  "label": "Submission Documents",
                  "rerender": true,
                  "maxFilesize": "20",
                  "defaultValue": [],
                  "acceptedFiles": ".pdf, .jpg, .jpeg, .png, .gif"
                }',
                '{
                  "en": "Submission Documents"
                }', 0,
                '749a361e-5bf1-11ee-943d-080027b7463b',
                '10000000-0000-0000-0000-000000000019', true);
    """

# This is taken from TEST
revert_config = """
        delete from cards_x_nodes_x_widgets where id = '6504d542-f1d8-4668-bd5b-e46e3e58b617';
    """


class Migration(migrations.Migration):
    dependencies = [
        ("bcrhp", "1036_update_heritage_site_export_config"),
    ]

    operations = [
        migrations.RunSQL(update_config, revert_config),
    ]
