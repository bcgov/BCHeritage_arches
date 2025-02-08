from django.db import migrations

add_value = """
    DO $$
        DECLARE
            top_concept_uuid uuid;
            top_collection_uuid uuid;
            child_values json;
            top_values json;
        BEGIN
            -- This needs to be well known to match with the IPA resource model node
            top_concept_uuid := get_concept_uuid('IPA Agreement Status', 'Concept');
            top_collection_uuid := get_concept_uuid('IPA Agreement Status', 'Collection');
            raise Notice 'Top concept: %', top_values;
            child_values := import_vocabulary_item_with_collection(
                    p_parent_concept_uuid => top_concept_uuid,
                    p_child_label => 'to be determined',
                            p_parent_collection_uuid := top_collection_uuid
                    );
        END $$;
    """

delete_value = """
   call delete_concept_and_children('to be determined');
"""

class Migration(migrations.Migration):
    dependencies = [
        ("bcfms", "1232_add_ipa_submission_types"),
    ]

    operations = [
        migrations.RunSQL(add_value, delete_value),
    ]
