create or replace view fossil_sample.storage_location_vw as
select sri.*,
       ri.location_name storage_location_name
from (select resourceinstanceid                                                      collected_sample_uuid,
             __bc_ref_from_tile(tiledata, fossil_sample.repository_name_nodeid())    repository_uuid,
             __bc_text_from_tile(tiledata, fossil_sample.storage_reference_nodeid()) storage_reference
      from tiles
      where nodegroupid = fossil_sample.repository_information_nodegroupid()) sri
         left join (select resourceinstanceid,
                           __bc_text_from_tile(tiledata,
                                               fossil_storage_location.storage_location_name_nodeid()) location_name
                    from tiles
                    where nodegroupid = fossil_storage_location.storage_location_name_nodegroupid()) ri
                   on sri.repository_uuid = ri.resourceinstanceid;
