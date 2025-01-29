from django.db import migrations
import os


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1111_add_missing_submission_documents_config")]

    fix_mv_chronology_index = """
       drop index if exists mv_chron_idx;
       create index mv_chron_idx on mv_chronology(resourceinstanceid);
        """

    reverse_fix_mv_chronology_index = """
       drop index if exists mv_chron_idx;
       create index mv_chron_idx on mv_protection_event(resourceinstanceid);
        """

    operations = [
        migrations.RunSQL(fix_mv_chronology_index, reverse_fix_mv_chronology_index),
    ]
