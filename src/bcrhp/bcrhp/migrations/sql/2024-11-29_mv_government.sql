create materialized view mv_government as
select resourceinstanceid, government_name->'en'->>'value' government_name,
       __arches_get_concept_label(government_type) government_type
from government.government_name;
create index gn_ri_idx on mv_government(resourceinstanceid);