create or replace view bcrhp_crhp_data_vw as
select distinct i.resourceinstanceid,
                i.descriptors site_descriptors,
                sn.site_names,
                bn.borden_number->'en'->>'value' borden_number,
                sos.sos,
                addr.addresses,
                st_srid(sb.site_boundary) site_boundary,
                st_astext(sb.site_boundary) boundary_geojson,
                st_x(st_centroid(sb.site_boundary)) site_centroid_longitude,
                st_y(st_centroid(sb.site_boundary)) site_centroid_latitude,
                st_area(sb.site_boundary::geography) area_sqm,
                hc.heritage_categories,
                hf.heritage_functions,
                se.significant_events,
                ca.construction_actors,
                ht.heritage_themes,
                __arches_get_concept_label(br.registration_status) registration_status,
                (select jsonb_agg(child_label) from get_uuid_lookup_table('Registry Type') where child_value_uuid = any(br.registry_types)) registry_types,
                br.officially_recognized_site,
                pe.protection_events,
                si.site_images,
                eu.external_urls
from heritage_site.instances i
         left join heritage_site.borden_number bn on bn.resourceinstanceid = i.resourceinstanceid
         left join (select resourceinstanceid, jsonb_agg( jsonb_build_object('name_type', __arches_get_concept_label(name_type), 'name', name->'en'->>'value')) site_names from heritage_site.site_names group by resourceinstanceid) sn on sn.resourceinstanceid = i.resourceinstanceid
         left join ( select resourceinstanceid,
                            jsonb_agg(
                                    jsonb_build_object(
                                            'significance_type', __arches_get_concept_label(significance_type),
                                            'defining_elements', defining_elements->'en'->>'value',
                                            'physical_description', physical_description->'en'->>'value',
                                            'document_location', document_location->'en'->>'value',
                                            'heritage_value', heritage_value->'en'->>'value'
                                        )
                                ) sos
                     from heritage_site.bc_statement_of_significance
                     group by resourceinstanceid
) sos on i.resourceinstanceid = sos.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_agg(jsonb_build_object(
                                   'street_address', street_address->'en'->>'value',
                                   'city', city->'en'->>'value',
                                   'locality', locality->'en'->>'value',
                                   'location_description', location_description->'en'->>'value'
                               )) addresses
                    from heritage_site.bc_property_address
                    group by resourceinstanceid) addr on i.resourceinstanceid = addr.resourceinstanceid
         left join heritage_site.site_boundary sb on i.resourceinstanceid = sb.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_agg(jsonb_build_object('ownership', __arches_get_concept_label(ownership),
                                                        'category', __arches_get_concept_label(heritage_category),
                                                        'contributing_resource_count', contributing_resource_count)) heritage_categories
                    from heritage_site.heritage_class
                    group by resourceinstanceid) hc
                   on i.resourceinstanceid = hc.resourceinstanceid
         left join (
    with c as (
        select resourceinstanceid, parent_label, child_label, unnest(functional_state) functional_state
        from heritage_site.heritage_function
                 join get_uuid_lookup_table('BC Heritage Function') lu
                      on lu.child_value_uuid = functional_category
    )
    select resourceinstanceid,
           jsonb_agg(jsonb_build_object('function_category', parent_label,
                                        'function_type', child_label,
                                        'function_state', __arches_get_concept_label(functional_state))) heritage_functions from c
    group by resourceinstanceid
) hf
                   on i.resourceinstanceid = hf.resourceinstanceid
         left join (select resourceinstanceid, jsonb_agg(jsonb_build_object('type', __arches_get_concept_label(construction_actor_type), 'name', construction_actor->'en'->>'value' )) construction_actors from heritage_site.construction_actors group by resourceinstanceid) ca
                   on i.resourceinstanceid = ca.resourceinstanceid
         left join (select resourceinstanceid, jsonb_agg( jsonb_build_object('category', parent_label , 'type', child_label)) heritage_themes
                    from heritage_site.heritage_theme
                             join get_uuid_lookup_table('BC Heritage Theme') lu
                                  on lu.child_value_uuid = any(heritage_theme.heritage_theme)
                    group by resourceinstanceid) ht
                   on i.resourceinstanceid = ht.resourceinstanceid
    -- @todo - sort these out
         left join heritage_site.bc_right br on i.resourceinstanceid = br.resourceinstanceid
         left join (select --prote.*,
                           prote.resourceinstanceid,
                           jsonb_agg(jsonb_build_object(
                                   'authority', __arches_get_concept_label(auth.authority),
                                   'legal_instrument', __arches_get_concept_label(auth.legal_instrument),
                                   'act_section', auth.act_section->'en'->>'value',
                                   'recognition_type', __arches_get_concept_label(auth.recognition_type),
                                   'government_name', govt.government_name->'en'->>'value',
                                   'reference_number', prote.reference_number->'en'->>'value',
                                   'designation_or_protection_start_date', prote.designation_or_protection_start_date)) protection_events
                    from heritage_site.protection_event prote
                             left join legislative_act.authority auth on (legislative_act[0]->>'resourceId')::uuid = auth.resourceinstanceid
                             left join government.government_name govt on (responsible_government[0]->>'resourceId')::uuid = govt.resourceinstanceid
                    group by prote.resourceinstanceid
) pe on i.resourceinstanceid = pe.resourceinstanceid
         left join (select resourceinstanceid,
                           (select jsonb_agg(
                                           jsonb_build_object(
                                                   'site_images', site_images,
                                                   'image_caption', bcrhp_build_image_caption(
                                                           __arches_get_concept_label(image_view),
                                                           image_features->'en'->>'value',
                                                           image_date
                                                       ),
                                                   'copyright', copyright->'en'->>'value',
                                                   'image_content_type', __arches_get_concept_label(image_view),
                                                   'image_type', __arches_get_concept_label(image_type),
                                                   'image_description', regexp_replace( image_description->'en'->>'value','<br>.*',''))
                                       )) site_images
                    from heritage_site.site_images where submit_to_crhp group by resourceinstanceid) si on i.resourceinstanceid = si.resourceinstanceid

         left join (select resourceinstanceid, jsonb_agg( jsonb_concat(jsonb_build_object('url_type',__arches_get_concept_label(external_url_type)), external_url)) external_urls from heritage_site.external_url group by resourceinstanceid) eu on i.resourceinstanceid = eu.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_agg(jsonb_build_object(
                                   'event_type', __arches_get_concept_label(chronology),
                                   'start_year', start_year,
                                   'end_year', end_year,
                                   'dates_approximate', dates_approximate
                               )) significant_events
                    from heritage_site.chronology group by resourceinstanceid) se on se.resourceinstanceid = i.resourceinstanceid;
