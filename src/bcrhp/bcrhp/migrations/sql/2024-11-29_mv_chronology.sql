create materialized view mv_chronology as
select resourceinstanceid,
       start_year,
       end_year,
       dates_approximate,
       __arches_get_concept_label(chronology) event,
       information_source->'en'->>'value' source,
       chronology_notes->'en'->>'value' event_notes
from heritage_site.chronology;
create index mv_chron_idx on mv_chronology(resourceinstanceid);