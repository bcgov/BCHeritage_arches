create view databc.fossil_sites_vw as
with child_names as (select pc.parent_id,
                            pc.child_id,
                            n.fossil_site_name -> 'en' ->> 'value' child_name
                     from (select resourceinstanceid                                                 parent_id,
                                  (jsonb_array_elements(ss.fossil_sub_sites) ->> 'resourceId')::uuid child_id
                           from fossil_site.fossil_sub_sites ss) pc
                              join fossil_site.fossil_site_name n on pc.child_id = n.resourceinstanceid)
select n.resourceinstanceid                                      site_id,
       n.fossil_site_name -> 'en' ->> 'value'                    site_name,
       ss.child_names                                            sub_site_names,
       l.location_description -> 'en' ->> 'value'                location_description,
       l.area_boundary                                           site_boundary,
       __arches_get_concept_label(src.significance_ranking_code) significance_ranking_code
from fossil_site.fossil_site_name n
         join fossil_site.bc_fossil_site_location l on n.resourceinstanceid = l.resourceinstanceid
         left join fossil_site.significance_ranking_code src on n.resourceinstanceid = src.resourceinstanceid
         left join (select parent_id, array_to_string(array_agg(child_name), '; ') child_names
                    from child_names
                    group by parent_id) ss on n.resourceinstanceid = ss.parent_id;