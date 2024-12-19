create materialized view mv_site_names as
select resourceinstanceid, __arches_get_concept_label(name_type) name_type,
       name->'en'->>'value' name
from heritage_site.site_names;
create index sn_idx on mv_site_names (resourceinstanceid);