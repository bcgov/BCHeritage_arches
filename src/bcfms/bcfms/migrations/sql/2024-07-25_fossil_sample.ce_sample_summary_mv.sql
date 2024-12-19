create materialized view fossil_sample.ce_sample_summary_mv as
with ce_samples_collected as (select resourceinstanceid collection_event_id,
                                     __bc_ref_from_tile(tiledata,
                                                        fossil_collection_event.samples_collected_nodeid()) samples_collected_uuid
                              from tiles
                              where nodegroupid = fossil_collection_event.samples_collected_nodegroupid())
select coll.collection_event_id,
       count(*) samples_collected,
       array_to_string(array_remove(array_agg(distinct slv.storage_location_name order by storage_location_name), null), '; ') storage_locations,
       array_to_string(array_remove(array_agg(distinct slv.storage_reference order by storage_reference), null), '; ') storage_references,
       array_to_string(array_remove(array_agg(distinct __bc_format_scientific_name(s1.name, s1.taxonomic_rank, s.name_connector, s2.name, s2.taxonomic_rank)
                                              order by __bc_format_scientific_name(s1.name, s1.taxonomic_rank, s.name_connector, s2.name, s2.taxonomic_rank)), ''),'; ') scientific_names,
       array_to_string(array_remove(array_agg(distinct cn.name order by cn.name),null), '; ') common_names,
       array_to_string(array_remove(array_agg(distinct s.size_category order by s.size_category), null), '; ') size_categories,
       array_to_string(array_remove(array_agg(distinct geological_group), ''), '; ') geological_groups,
       array_to_string(array_remove(array_agg(distinct geological_formation), ''), '; ') geological_formations,
       array_to_string(array_remove(array_agg(distinct geological_member), ''), '; ') geological_members,
       array_to_string(array_remove(array_agg(distinct informal_name), ''), '; ') informal_names,
       array_to_string(array_remove(array_agg(distinct other_name), ''), '; ') other_names,
       min(time_scale) time_scale,  -- Geological Age is a 1:1 with fossil sample, so just use the min values
       min(minimum_time) minimum_time,
       min(maximum_time) maximum_time
from ce_samples_collected coll
         left join fossil_sample.geological_age_vw ga on coll.samples_collected_uuid = ga.fossil_sample_uuid
         left join fossil_sample.stratigraphy_vw strat on coll.samples_collected_uuid = strat.fossil_sample_uuid,
     fossil_sample.fossil_name_mv s
         left join fossil_type.fossil_name_mv s1 on s.scientific_name = s1.fossil_name_uuid
         left join fossil_type.fossil_name_mv s2 on s.other_scientific_name = s2.fossil_name_uuid
         left join fossil_type.fossil_name_mv cn on s.common_name = cn.fossil_name_uuid
         left join fossil_sample.storage_location_vw slv on s.fossil_sample_uuid = slv.collected_sample_uuid
where coll.samples_collected_uuid = s.fossil_sample_uuid
group by coll.collection_event_id;
create unique index ce_sample_summary_idx1 on fossil_sample.ce_sample_summary_mv(collection_event_id);
