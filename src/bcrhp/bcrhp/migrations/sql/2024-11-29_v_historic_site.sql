create or replace view V_HISTORIC_SITE as
select distinct bn.resourceinstanceid,
                bn.borden_number,
                br.officially_recognized_site,
                br.registration_status registration_status,
                cn.name common_name,
                array_to_string(other_name.names, '; ') other_name,
                prop.pid,
                prop.street_address,
                prop.city,
                prop.postal_code,
                prop.province,
                prop.locality,
                prop.location_description,
                br.authorities,
                mc.chronology,
                significance_statement,
                ca.actors,
                hf.functional_states,
                ht.heritage_theme,
                hc.heritage_class,
                msb.area_sqm::numeric(19,2) dimensions_area_sqm,
                msb.site_centroid_latitude::numeric(10,6) gis_latitude,
                msb.site_centroid_longitude::numeric(10,6) gis_longitude,
                msb.utmzone::numeric(2,0) utm_zone,
                msb.utmnorthing::numeric(10,0) utm_northing,
                msb.utmeasting::numeric(10,0) utm_easting,
                'https://apps.nrs.gov.bc.ca/int/bcrhp/report/'||bn.resourceinstanceid site_url,
                msb.site_boundary,
                msra.bcrhp_submission_status,
                msra.restricted,
                msra.date_submitted_to_crhp
from mv_borden_number bn
         left join (
    select resourceinstanceid, name
    from mv_site_names where name_type = 'Common'
) cn on cn.resourceinstanceid = bn.resourceinstanceid
         left join (
    select resourceinstanceid, array_agg(name) names
    from mv_site_names
    where name_type = 'Other'
    group by resourceinstanceid
) other_name on other_name.resourceinstanceid = bn.resourceinstanceid
         join (
    select distinct
        r.resourceinstanceid,
        r.officially_recognized_site,
        r.registration_status,
        jsonb_agg(
                case when pe.authority is null then null else
                    jsonb_build_object(
                            'authority', pe.authority,
                            'auth_order', databc.authority_priority(pe.authority),
                            'start_date', pe.designation_or_protection_start_date,
                            'end_date', pe.designation_or_protection_end_date,
                            'government_name', pe.government_name,
                            'recognition_type', pe.recognition_type,
                            'reference_number', pe.reference_number,
                            'registry_types', r.registry_types
                        ) end order by databc.authority_priority(pe.authority) desc,
                    designation_or_protection_start_date desc
            )->0 authorities
    from mv_bc_right r
             left join mv_site_protection_event pe on r.bc_right_id = pe.bc_right_id
    group by r.resourceinstanceid, r.officially_recognized_site, r.registration_status
) br on bn.resourceinstanceid = br.resourceinstanceid
         join mv_site_record_admin msra on bn.resourceinstanceid = msra.resourceinstanceid
         left join (
    select resourceinstanceid,
           jsonb_agg(
                   jsonb_build_object(
                           'start_year', start_year,
                           'end_year', end_year,
                           'dates_approximate', dates_approximate,
                           'event', event,
                           'source', source,
                           'event_notes', event_notes
                       ) order by start_year
               ) chronology
    from mv_chronology
    group by resourceinstanceid
) mc on bn.resourceinstanceid = mc.resourceinstanceid
         left join (
    select resourceinstanceid,
           jsonb_object_agg(state_period, array_to_string(functional_states, '; ') ) functional_states
    from mv_heritage_function
    group by resourceinstanceid
) hf on bn.resourceinstanceid = hf.resourceinstanceid
         left join (
    select resourceinstanceid,
           array_to_string(array_agg(heritage_theme), '; ') heritage_theme
    from mv_heritage_theme
    group by resourceinstanceid
) ht on bn.resourceinstanceid = ht.resourceinstanceid
         left join (
    select resourceinstanceid,
           string_agg(
                                           (elm->>'category')::text || ' ' ||
                                           '(' || (elm->>'ownership')::text || ', ' ||
                                           (elm->>'resource_count') || ')',
                                           ', '
               ) heritage_class
    from mv_heritage_class, jsonb_array_elements(heritage_class) elm
    group by resourceinstanceid
) hc on bn.resourceinstanceid = hc.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_object_agg(
                                   actor_type, jsonb_build_object('actors', array_to_string(actors, '; '), 'notes', array_to_string(notes, '; ') )
                               ) actors
                    from mv_construction_actors
                    group by resourceinstanceid order by resourceinstanceid
) ca on bn.resourceinstanceid = ca.resourceinstanceid
         left join mv_site_boundary msb on bn.resourceinstanceid = msb.resourceinstanceid
         left join (
    select resourceinstanceid,
           jsonb_agg(
                   jsonb_build_object(
                           'significance_type', databc.html_to_plain_string(significance_type),
                           'significance_level', databc.authority_priority(significance_type),
                           'physical_description', databc.html_to_plain_string(physical_description),
                           'defining_elements', databc.html_to_plain_string(defining_elements),
                           'heritage_value', databc.html_to_plain_string(heritage_value),
                           'document_location', databc.html_to_plain_string(document_location)
                       )
                   order by databc.authority_priority(significance_type) desc
               )->0 significance_statement
    from mv_bc_statement_of_significance
    group by resourceinstanceid
) sos on bn.resourceinstanceid = sos.resourceinstanceid
         left join mv_unique_property_address prop on bn.resourceinstanceid = prop.resourceinstanceid;
