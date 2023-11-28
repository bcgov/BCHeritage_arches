select __arches_create_resource_model_views(graphid)
from graphs
where isresource = true
  and publicationid is not null
  and name->>'en' != 'Arches System Settings';

create or replace function get_uuid_lookup_table(parent_name text, language_code text[] default array['en', 'en-US'])
    returns table(parent_label text, parent_concept_uuid uuid, parent_value_uuid uuid, child_label text, child_concept_uuid uuid, child_value_uuid uuid) as
$$
declare
begin
    return query with recursive concept_hierarchy as (
        select null parent_value, null::uuid parent_concept_uuid, null::uuid parent_value_uuid,
               v.value child_value, v.conceptid child_concept_uuid, v.valueid child_value_uuid
        from concepts c,
             values v,
             relations r
        where c.conceptid = v.conceptid
          and r.conceptidto = c.conceptid
          and nodetype = 'Concept'
          and v.value = parent_name
          and v.languageid = any(language_code)
          and r.relationtype = 'hasTopConcept'
        UNION ALL
        select parent_v.value    parent_value,
               parent_v.conceptid  parent_concept_uuid,
               parent_v.valueid  parent_value_uuid,
               child_v.value     child_value,
               child_v.conceptid child_concept_uuid,
               child_v.valueid child_value_uuid
        from relations child
                 JOIN concept_hierarchy hier on hier.child_concept_uuid = child.conceptidfrom,
             concepts child_c,
             values child_v,
             values parent_v
        where child_c.conceptid = child_v.conceptid
          and child.conceptidto = child_c.conceptid
          and nodetype = 'Concept'
          and hier.child_concept_uuid = parent_v.conceptid
          and child.relationtype in ('member','narrower')
          and child_v.valuetype = 'prefLabel'
          and parent_v.valuetype = 'prefLabel'
          and child_v.languageid = parent_v.languageid
          and parent_v.languageid = any (language_code)
    )
                 select distinct *
                 from concept_hierarchy order by parent_value, child_value;
end $$
    language plpgsql;


create view bcrhp_crhp_data_vw as
select distinct i.resourceinstanceid,
       i.descriptors site_descriptors,
       bn.borden_number->'en'->>'value' borden_number,
       sos.defining_elements->'en'->>'value' defining_elements,
       sos.physical_description->'en'->>'value' physical_description,
       sos.document_location->'en'->>'value' document_location,
       sos.heritage_value->'en'->>'value' heritage_value,
--        addr.*,
       addr.street_address->'en'->>'value' street_address,
       addr.city->'en'->>'value' city,
       addr.locality->'en'->>'value' locality,
       addr.location_description->'en'->>'value' location_description,
--        sb.*,
       st_srid(sb.site_boundary) site_boundary,
       st_astext(sb.site_boundary) boundary_geojson,
       st_area(sb.site_boundary::geography) area_sqm,
--        hc.*,
--        (select child_label from get_uuid_lookup_table('Ownership Type') where child_value_uuid = hc.ownership) ownership,
       __arches_get_concept_label(hc.ownership) ownership,
--        (select child_label from get_uuid_lookup_table('Heritage Category') where child_value_uuid = hc.heritage_category) heritage_category,
       __arches_get_concept_label(hc.heritage_category) heritage_category,
       hc.contributing_resource_count,
--        hf.*,
       __arches_get_concept_label(hf.functional_category) functional_category,
--        hf.functional_state,
       (select jsonb_agg(child_label) from get_uuid_lookup_table('BC Functional Status') where child_value_uuid = any(hf.functional_state)) functional_state,
--        ht.*,

       (select jsonb_agg(child_label) from get_uuid_lookup_table('BC Heritage Theme') where child_value_uuid = any(ht.heritage_theme)) heritage_themes,
--         br.*,
--         br.registration_status,
       __arches_get_concept_label(br.registration_status) registration_status,
--         br.registry_types,

--        __arches_get_concept_list_label(br.registry_types) registry_types,
       (select jsonb_agg(child_label) from get_uuid_lookup_table('Registry Type') where child_value_uuid = any(br.registry_types)) registry_types,
       br.officially_recognized_site,
--         pe.*,
--         pe.legislative_act,
--         pe.authority,
       __arches_get_concept_label(pe.authority) authority,
--         pe.legal_instrument,
       __arches_get_concept_label(pe.legal_instrument) legal_instrument,
       pe.act_section->'en'->>'value' act_section,
--         pe.recognition_type,
       __arches_get_concept_label(pe.recognition_type) recognition_type,
--         pe.responsible_government,
       pe.government_name->'en'->>'value' responsible_government_name,
       pe.reference_number->'en'->>'value' reference_number,
       pe.designation_or_protection_start_date,
--         si.*,
       si.site_images,
--        si.site_images,
--        si.image_caption->'en'->>'value' image_caption,
--        si.copyright->'en'->>'value' copyright,
-- --         si.image_content_type,
--        __arches_get_concept_label(si.image_content_type) image_content_type,
--        si.image_description->'en'->>'value' image_description,
--         eu.*,
       __arches_get_concept_label(eu.external_url_type) external_url_type,
       eu.external_url
from heritage_site.instances i
         left join heritage_site.borden_number bn on bn.resourceinstanceid = i.resourceinstanceid
         left join heritage_site.bc_statement_of_significance sos on i.resourceinstanceid = sos.resourceinstanceid
         left join heritage_site.bc_property_address addr on i.resourceinstanceid = addr.resourceinstanceid
         left join heritage_site.site_boundary sb on i.resourceinstanceid = sb.resourceinstanceid
         left join heritage_site.heritage_class hc on i.resourceinstanceid = hc.resourceinstanceid
         left join heritage_site.heritage_function hf on i.resourceinstanceid = hf.resourceinstanceid
         left join heritage_site.heritage_theme ht on i.resourceinstanceid = ht.resourceinstanceid
    -- @todo - sort these out
         left join heritage_site.bc_right br on i.resourceinstanceid = br.resourceinstanceid
         left join (select prote.*, auth.authority, auth.legal_instrument,auth.act_section, auth.recognition_type,
                           govt.government_name
                    from heritage_site.protection_event prote
                             left join legislative_act.authority auth on (legislative_act[0]->>'resourceId')::uuid = auth.resourceinstanceid
                             left join government.government_name govt on (responsible_government[0]->>'resourceId')::uuid = govt.resourceinstanceid
) pe on i.resourceinstanceid = pe.resourceinstanceid
         left join (select resourceinstanceid,
                           (select jsonb_agg(
                                           jsonb_build_object(
                                                   'site_images', site_images, 'image_caption', image_caption->'en'->>'value', 'copyright', copyright->'en'->>'value',
                                                   'image_content_type', __arches_get_concept_label(image_content_type), 'image_description', image_description->'en'->>'value')
                                       )) site_images
    from heritage_site.site_images where submit_to_crhp group by resourceinstanceid) si on i.resourceinstanceid = si.resourceinstanceid

         left join heritage_site.external_url eu on i.resourceinstanceid = eu.resourceinstanceid;
