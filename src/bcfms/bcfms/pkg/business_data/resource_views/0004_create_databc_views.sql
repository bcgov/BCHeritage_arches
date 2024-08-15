drop function if exists __bc_format_uncertainty(text, boolean);
create or replace function __bc_format_uncertainty(value text, value_uncertain boolean) returns text as
$$
DECLARE
BEGIN
    return value || (case when value_uncertain then ' ?' else '' end);
END $$ language plpgsql;

create or replace view databc.important_fossil_areas_vw as
    select n.resourceinstanceid area_id,
           n.area_name->'en'->>'value' area_name,
           n.description->'en'->>'value' description,
           b.area_boundary area_boundary from important_fossil_area.area_name n
        join important_fossil_area.area_boundary b on n.resourceinstanceid = b.resourceinstanceid;

create view databc.fossil_sites_vw as
with child_names as (
select pc.parent_id,
       pc.child_id,
    n.fossil_site_name->'en'->>'value' child_name
    from (select resourceinstanceid parent_id,
       (jsonb_array_elements(ss.fossil_sub_sites)->>'resourceId')::uuid child_id from fossil_site.fossil_sub_sites ss) pc
        join fossil_site.fossil_site_name n on pc.child_id = n.resourceinstanceid)
select n.resourceinstanceid site_id,
       n.fossil_site_name->'en'->>'value' site_name,
       ss.child_names sub_site_names,
       l.location_description->'en'->>'value' location_description,
       l.area_boundary site_boundary,
       __arches_get_concept_label(src.significance_ranking_code) significance_ranking_code
from fossil_site.fossil_site_name n
    join fossil_site.bc_fossil_site_location l on n.resourceinstanceid = l.resourceinstanceid
    left join fossil_site.significance_ranking_code src on n.resourceinstanceid = src.resourceinstanceid
    left join (select parent_id, array_to_string(array_agg(child_name), '; ') child_names from child_names group by parent_id) ss on n.resourceinstanceid = ss.parent_id;


create or replace view databc.provincially_protected_fossil_sites_vw as
with area_boundaries as (select resourceinstanceid,
                                st_collect(array_agg(area_boundary))  area_boundaries,
                                cardinality(array_agg(area_boundary)) geometry_count
                         from provincially_protected_fossil_site.area_boundary
                         group by resourceinstanceid)
select n.resourceinstanceid                                                                            site_id,
       n.site_name -> 'en' ->> 'value'                                                                 site_name,
       n.description -> 'en' ->> 'value'                                                               site_description,
       __arches_get_concept_label(ps.protection_status) protection_status,
       l.area_boundaries,
       pda.location_description -> 'en' ->> 'value',
       __arches_get_concept_label(ga.geologic_timescale_division)                                      geologic_timescale_division,
       __bc_format_uncertainty(__arches_get_concept_label(ga.minimum_time), ga.minimum_time_uncertain) minimum_time,
       __bc_format_uncertainty(__arches_get_concept_label(ga.maximum_time), ga.maximum_time_uncertain) maximum_time,
       __bc_format_uncertainty(__arches_get_concept_label(geological_group),geological_group_uncertain) geologic_group,
       __bc_format_uncertainty(__arches_get_concept_label(geological_formation), geological_formation_uncertain) geologic_formation,
       __bc_format_uncertainty(__arches_get_concept_label(geological_member),geological_member_uncertain) geologic_member
from provincially_protected_fossil_site.site_name n
         join area_boundaries l on n.resourceinstanceid = l.resourceinstanceid
         left join provincially_protected_fossil_site.protection_status ps
                   on n.resourceinstanceid = ps.resourceinstanceid
         left join provincially_protected_fossil_site.place_description_assignment pda
                   on n.resourceinstanceid = pda.resourceinstanceid
         left join provincially_protected_fossil_site.geological_age ga on n.resourceinstanceid = ga.resourceinstanceid
         left join provincially_protected_fossil_site.stratigraphy s on n.resourceinstanceid = s.resourceinstanceid;

create or replace view databc.collection_events_vw as
select row_uuid,
       collection_event_id,
       collection_start_year,
       array_to_string(collector_names, ', ') collectors,
       location_descriptor,
       collection_event_significant,
       common_names,
       scientific_names,
       fossil_abundance,
       size_categories,
       time_scale,
       minimum_time,
       maximum_time,
       geological_groups,
       geological_formations,
       geological_members,
       publication_count,
       publication_years,
       publication_types,
       authors
from fossil_collection_event.collection_event_vw;
