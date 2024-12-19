create or replace view fossil_collection_event.collection_event_vw as
with ce_collection_details as (select * from tiles where nodegroupid = fossil_collection_event.collection_start_year_nodegroupid()),
     ce_location as (select * from tiles where nodegroupid = fossil_collection_event.collection_location_nodegroupid()),
     ce_abundance as (select * from tiles where nodegroupid = fossil_collection_event.fossil_abundance_nodegroupid()),
     ce_significant as (select * from tiles where nodegroupid = fossil_collection_event.collection_event_significant_nodegroupid())
select
    uuid_generate_v4() row_uuid,
    ced.resourceinstanceid collection_event_id,
    coalesce(__arches_get_node_display_value(ced.tiledata, fossil_collection_event.collection_start_year_nodeid()), '') collection_start_year,
    __bc_text_from_tile(cel.tiledata, fossil_collection_event.location_descriptor_nodeid()) location_descriptor,
    __bc_point_from_tile(cel.tiledata, fossil_collection_event.collection_location_nodeid()) collection_location,
    __arches_get_node_display_value(cea.tiledata, fossil_collection_event.fossil_abundance_nodeid()) fossil_abundance,
    coalesce((cea.tiledata->>fossil_collection_event.collection_event_significant_nodeid()::text)::boolean, false) collection_event_significant,
--     st_asgeojson(cel.tiledata->>'collection_location')::jsonb->'coordinates'->0 "Collection Location",
--     __arches_get_node_display_value(cel.tiledata, fossil_collection_event.collection_location_nodeid()),
--     cesc.samples_collected_uuid,
    coll.collector_ids,
    coll.collector_names,
    ce_sample_summary.storage_locations,
    ce_sample_summary.storage_references,
    ce_sample_summary.scientific_names,
    ce_sample_summary.common_names,
    ce_sample_summary.size_categories,
    ce_sample_summary.geological_groups,
    ce_sample_summary.geological_formations,
    ce_sample_summary.geological_members,
    ce_sample_summary.informal_names,
    ce_sample_summary.other_names,
    coalesce(ce_sample_summary.time_scale,'') time_scale,
    coalesce(ce_sample_summary.minimum_time,'') minimum_time,
    coalesce(ce_sample_summary.maximum_time,'') maximum_time,
    coalesce(pub_summ.publication_count, 0) publication_count,
    coalesce(pub_summ.publication_years, '') publication_years,
    coalesce(pub_summ.publication_types,'')  publication_types,
    coalesce(pub_summ.authors,'')  authors
--     ,*
from ce_collection_details ced
         left join fossil_sample.ce_sample_summary_mv ce_sample_summary on ce_sample_summary.collection_event_id = ced.resourceinstanceid
         left join ce_location cel on cel.parenttileid = ced.tileid
         left join publication.ce_publication_summary_mv pub_summ on pub_summ.collection_event = ced.resourceinstanceid
         left join fossil_collection_event.collectors_vw coll on coll.collection_event_id = ced.resourceinstanceid
         left join ce_abundance cea on cea.resourceinstanceid = ced.resourceinstanceid
         left join ce_significant ces on ces.resourceinstanceid = ced.resourceinstanceid;
