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
