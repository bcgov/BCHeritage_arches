# Generated by Django 4.2.13 on 2024-06-18 11:16

from django.db import migrations
from bcrhp.migrations.operations.privileged_sql import RunPrivilegedSQL


class Migration(migrations.Migration):

    dependencies = [
        ('bcrhp', '0008_public_internal_map_layers_665'),
    ]

    operations = [
        RunPrivilegedSQL(
            """
            update map_layer set sortorder = 1 where name = 'Cadastral ParcelMap';
            update map_layer set sortorder = 2 where name = 'Municipal Boundaries';
            update map_layer set sortorder = 3 where name = 'Regional District Boundaries';
            update map_layer set sortorder = 4 where name = 'Indigenous Reserves and Band Names';
            update map_layer set sortorder = 5 where name = 'Islands Trust Administrative Boundaries';
            update map_layer set sortorder = 6 where name = 'Local Trust Administrative Boundaries';
            update map_layer set sortorder = 7 where name = 'Tourism Regions';
            update map_layer set sortorder = 8 where name = 'Digital Road Atlas';
            update map_layer set sortorder = 9 where name = 'Trim Water Lines';
            update map_layer set sortorder = 10 where name = 'Lakes';
            update map_layer set sortorder = 11 where name = 'Crown tenures';
            update map_layer set sortorder = 12 where name = 'Tantalis Surveyed Parcels';
            update map_layer set sortorder = 13 where name = 'National parks';
            update map_layer set sortorder = 14 where name = 'Provincial Parks';
            update map_layer set sortorder = 15 where name = 'Municipal Parks';
            update map_layer set sortorder = 16 where name = 'Borden Grid';
            update map_layer set sortorder = 17 where name = 'Heritage Sites';
            """,
            """
            update map_layer set sortorder = 0;
            """)
    ]