create or replace view fossil_collection_event.collectors_vw as
with ce_collectors as (select resourceinstanceid collection_event_id,
                              __bc_ref_from_tile(tiledata, fossil_collection_event.collectors_nodeid()) collector_id
                       from tiles
                       where nodegroupid = fossil_collection_event.collectors_nodegroupid())
select coll.collection_event_id,
       array_agg(collector_id) collector_ids,
       array_agg((cont.contributor_name -> 'en' ->> 'value') || ', ' || (cont.first_name -> 'en' ->> 'value')) collector_names
from ce_collectors coll
         join contributor.contributor cont on coll.collector_id = cont.resourceinstanceid
group by coll.collection_event_id;