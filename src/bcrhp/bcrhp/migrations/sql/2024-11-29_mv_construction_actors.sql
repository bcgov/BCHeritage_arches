create materialized view mv_construction_actors as
select resourceinstanceid,
       __arches_get_concept_label(construction_actor_type) actor_type,
       array_agg(construction_actor->'en'->>'value') actors,
       array_remove(array_agg(construction_actor_notes->'en'->>'value'),'') notes
from heritage_site.construction_actors
group by resourceinstanceid, __arches_get_concept_label(construction_actor_type);
create index mv_ca_idx on mv_construction_actors(resourceinstanceid);