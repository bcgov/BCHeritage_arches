create materialized view mv_heritage_theme as
select resourceinstanceid,
       __arches_get_concept_label(unnest(heritage_theme)) heritage_theme
from heritage_site.heritage_theme
group by resourceinstanceid,
         __arches_get_concept_label(unnest(heritage_theme));
create index mv_ht_idx on mv_heritage_theme (resourceinstanceid);