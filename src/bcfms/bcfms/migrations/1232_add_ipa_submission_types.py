from django.db import migrations

add_concepts = """
    DO $$
        DECLARE
            scheme_uuid uuid;
            top_collection_uuid uuid;
            value text;
            child_values json;
            requirements text[] = array['Chance Find Protocol',
                                        'Fossil Impact Assessment',
                                        'Fossil Impact Assessment Plan',
                                        'Impact Mitigation Final Report',
                                        'Impact Mitigation Plan',
                                        'Other Requirement',
                                        'Preliminary Study Report',
                                        'Site Assessment Final Report',
                                        'Site Assessment Plan'];
            top_values json;
        BEGIN
            -- This needs to be well known to match with the IPA resource model node
            top_collection_uuid := '6e1cdc31-0f16-4bd0-8fcc-b3246a808295'::uuid;
            scheme_uuid := get_concept_uuid('BC Fossils Thesauri', 'ConceptScheme');
            top_values := import_vocabulary_item_with_collection(
                    p_parent_concept_uuid => scheme_uuid,
                    p_child_label => 'IPA Project Requirement',
                    p_concept_relationship => 'hasTopConcept',
                    p_parent_collection_uuid => null,
                          p_child_collection_uuid => top_collection_uuid);
            raise Notice 'Top values: %', top_values;
            foreach value in ARRAY requirements loop
                    child_values := import_vocabulary_item_with_collection(
                            p_parent_concept_uuid => (top_values->>'concept_id')::uuid,
                            p_child_label => value,
                            p_parent_collection_uuid => (top_values->>'collection_id')::uuid);
                end loop;
        END $$;
    """

delete_concepts = """
   call delete_concept_and_children('IPA Project Requirement');
   """

class Migration(migrations.Migration):
    dependencies = [
        ("bcfms", "1222_disable_download_email_notifications"),
        ("bcgov_arches_common", "2025-02-07_create_concept_functions"),
    ]

    operations = [
        migrations.RunSQL(add_concepts, delete_concepts),
    ]
