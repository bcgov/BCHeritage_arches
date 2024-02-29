-- Materialized views to support the Data BC export
drop materialized view if exists mv_borden_number cascade;
create materialized view mv_borden_number as
select resourceinstanceid, borden_number->'en'->>'value' borden_number from heritage_site.borden_number;
create index bn_idx on mv_borden_number (resourceinstanceid);

drop materialized view if exists mv_site_names;
create materialized view mv_site_names as
select resourceinstanceid, __arches_get_concept_label(name_type) name_type,
       name->'en'->>'value' name
from heritage_site.site_names;
create index sn_idx on mv_site_names (resourceinstanceid);

drop materialized view if exists mv_bc_statement_of_significance cascade;
create materialized view mv_bc_statement_of_significance as
select resourceinstanceid,
       defining_elements->'en'->>'value' defining_elements,
       physical_description->'en'->>'value' physical_description,
       document_location->'en'->>'value' document_location,
       __arches_get_concept_label(significance_type) significance_type,
       heritage_value->'en'->>'value' heritage_value
from heritage_site.bc_statement_of_significance sos;
create index sos_ri_idx1 on mv_bc_statement_of_significance(resourceinstanceid);

-- select * from mv_property_address;
drop materialized view if exists mv_property_address cascade;
create materialized view mv_property_address as
select resourceinstanceid,
       tileid property_address_id,
       street_address->'en'->>'value' street_address,
       city->'en'->>'value' city,
       __arches_get_concept_label(province) province,
       postal_code->'en'->>'value' postal_code,
       locality->'en'->>'value' locality,
       location_description->'en'->>'value' location_description
from heritage_site.bc_property_address pa;
create index pa_ri_idx1 on mv_property_address(resourceinstanceid);
create index pa_ri_idx2 on mv_property_address(resourceinstanceid, property_address_id);

-- select * from mv_legal_description;
drop materialized view if exists mv_legal_description cascade;
create materialized view mv_legal_description as
select resourceinstanceid,
       bc_property_address,
       pid,
       pin,
       legal_description->'en'->>'value' legal_description
from heritage_site.bc_property_legal_description ld;
create index ld_ri_idx on mv_legal_description(resourceinstanceid, bc_property_address);


drop materialized view if exists mv_bc_right;
create materialized view mv_bc_right as
with unnested as (
select resourceinstanceid,
       tileid bc_right_id,
       officially_recognized_site,
       __arches_get_concept_label(registration_status) registration_status,
       unnest(registry_types)  registry_type
        from heritage_site.bc_right)
select resourceinstanceid,
       bc_right_id,
       officially_recognized_site,
       registration_status,
       array_agg(__arches_get_concept_label(registry_type)) registry_types from unnested
group by resourceinstanceid,
         bc_right_id,
         officially_recognized_site,
        registration_status;
create index br_ri_idx on mv_bc_right(resourceinstanceid, bc_right_id);

drop materialized view if exists mv_government cascade;
create materialized view mv_government as
select resourceinstanceid, government_name->'en'->>'value' government_name,
       __arches_get_concept_label(government_type) government_type
from government.government_name;
create index gn_ri_idx on mv_government(resourceinstanceid);
-- left join government.government_name gn on (pe.responsible_government[0]->>'resourceId')::uuid = gn.resourceinstanceid;

drop materialized view if exists mv_protection_event cascade;
create materialized view mv_protection_event as
select pe.resourceinstanceid,
       bc_right bc_right_id,
       (pe.legislative_act[0]->>'resourceId')::uuid legislative_act_id,
       (pe.responsible_government[0]->>'resourceId')::uuid government_id,
       designation_or_protection_start_date,
       designation_or_protection_end_date,
       reference_number->'en'->>'value' reference_number,
       protection_notes->'en'->>'value' protection_notes
from heritage_site.protection_event pe;
create index pe_ri_fk_idx on mv_protection_event(resourceinstanceid, legislative_act_id, government_id);

drop materialized view if exists mv_site_protection_event cascade;
create materialized view mv_site_protection_event as
select pe.resourceinstanceid,
       bc_right_id,
       designation_or_protection_start_date,
       designation_or_protection_end_date,
       reference_number,
       protection_notes,
       __arches_get_concept_label(la.authority) authority,
       __arches_get_concept_label(la.legal_instrument) legal_instrument,
       la.act_section->'en'->>'value' act_section,
       __arches_get_concept_label(la.recognition_type) recognition_type,
       gn.government_name,
       gn.government_type
--        gn.government_type->'en'->>'value' government_type
from mv_protection_event pe
    join legislative_act.authority la on legislative_act_id = la.resourceinstanceid
    left join mv_government gn on pe.government_id = gn.resourceinstanceid;
create index mv_pe_idx on mv_site_protection_event(resourceinstanceid, bc_right_id);

drop materialized view if exists mv_chronology;
create materialized view mv_chronology as
select resourceinstanceid,
       start_year,
       end_year,
       dates_approximate,
       __arches_get_concept_label(chronology) event,
       information_source->'en'->>'value' source,
       chronology_notes->'en'->>'value' event_notes
from heritage_site.chronology;
create index mv_chron_idx on mv_protection_event(resourceinstanceid);

drop materialized view if exists mv_site_record_admin cascade;
create materialized view mv_site_record_admin as
select resourceinstanceid,
       restricted,
       __arches_get_concept_label(bcrhp_submission_status) bcrhp_submission_status,
       __arches_get_concept_label(crhp_submission_status) crhp_submission_status,
       date_submitted_to_crhp,
       federal_id_number
from heritage_site.site_record_admin;
create index mv_sra_idx on mv_site_record_admin(resourceinstanceid);
create index mv_sra_idx2 on mv_site_record_admin(bcrhp_submission_status);

drop materialized view if exists mv_heritage_function cascade;
create materialized view mv_heritage_function as
    select resourceinstanceid,
           __arches_get_concept_label(unnest(functional_state)) state_period,
           array_agg(__arches_get_concept_label(functional_category))  functional_states
    from heritage_site.heritage_function group by resourceinstanceid,
                                                  __arches_get_concept_label(unnest(functional_state));
create index mv_hf_idx on mv_heritage_function(resourceinstanceid);

drop materialized view if exists mv_construction_actors cascade;
create materialized view mv_construction_actors as
select resourceinstanceid,
       __arches_get_concept_label(construction_actor_type) actor_type,
       array_agg(construction_actor->'en'->>'value') actors
        from heritage_site.construction_actors
group by resourceinstanceid, __arches_get_concept_label(construction_actor_type);
create index mv_ca_idx on mv_construction_actors(resourceinstanceid);

create or replace function bc_get_utm_zone(point geometry) returns int as
$$
DECLARE
BEGIN
    return int4(ceil((st_x(st_centroid(point)) + 180.0) / 6));
end;$$ language plpgsql;

create or replace function bc_get_utm_srid(point geometry) returns int as
$$
DECLARE
BEGIN
    return 26900 + bc_get_utm_zone(point);
end;$$ language plpgsql;

create or replace function bc_get_utm_northing(point geometry) returns int as
$$
DECLARE
BEGIN
    return trunc(st_y(st_transform(point, bc_get_utm_srid(point))));
EXCEPTION when others then
    raise notice 'Unable to get northing for srid %', bc_get_utm_srid(point);
    return null;
end;$$ language plpgsql;

create or replace function bc_get_utm_easting(point geometry) returns int as
$$
DECLARE
BEGIN
    return trunc(st_x(st_transform(point, bc_get_utm_srid(point))));
EXCEPTION when others then
    raise notice 'Unable to get easting for srid %', bc_get_utm_srid(point);
    return null;
end;$$ language plpgsql;


drop materialized view if exists mv_site_boundary cascade;
create materialized view mv_site_boundary as
select b.resourceinstanceid,
       site_boundary,
       st_area(site_boundary::geography) area_sqm,
       st_y(st_centroid(site_boundary)) site_centroid_latitude,
       st_x(st_centroid(site_boundary)) site_centroid_longitude,
       bc_get_utm_zone(st_centroid(site_boundary)) utmzone,
       bc_get_utm_northing(st_centroid(site_boundary)) utmnorthing,
       bc_get_utm_easting(st_centroid(site_boundary)) utmeasting
       from heritage_site.site_boundary b join heritage_site.borden_number bn on b.resourceinstanceid = bn.resourceinstanceid;

create index mv_sb_idx on mv_site_boundary(resourceinstanceid);

create or replace procedure refresh_materialized_views() as
$$
BEGIN
    refresh materialized view mv_bc_right;
    refresh materialized view mv_bc_statement_of_significance;
    refresh materialized view mv_borden_number;
    refresh materialized view mv_chronology;
    refresh materialized view mv_construction_actors;
    refresh materialized view mv_government;
    refresh materialized view mv_heritage_function;
    refresh materialized view mv_legal_description;
    refresh materialized view mv_property_address;
    refresh materialized view mv_protection_event;
    refresh materialized view mv_geojson_geoms;
    refresh materialized view mv_site_boundary;
    refresh materialized view mv_site_names;
    refresh materialized view mv_site_protection_event;
    refresh materialized view mv_site_record_admin;
END
$$ language plpgsql;

create schema if not exists databc;

drop function if exists databc.get_first_address cascade;
create or replace function databc.get_first_address(p_resourceinstanceid uuid) returns
    TABLE(resourceinstanceid uuid,
          property_address_id uuid,
          street_address text,
          city text,
          province text,
          postal_code text,
          locality text,
          location_description text,
          pid text,
          pin text,
          legal_description text) as
$$
BEGIN
    return query select mpa.resourceinstanceid,
                        mpa.property_address_id,
                        mpa.street_address,
                        mpa.city,
                        mpa.province,
                        mpa.postal_code,
                        mpa.locality,
                        mpa.location_description,
                        case when mld.pid = 0 then null else lpad(mld.pid::text,9,'0') end pid,
                        case when mld.pin = 0 then null else lpad(mld.pin::text,9,'0') end pin,
                        mld.legal_description
                 from mv_property_address mpa
                          left join mv_legal_description mld
                                    on mpa.property_address_id = mld.bc_property_address
                 where mpa.resourceinstanceid = p_resourceinstanceid
                 limit 1;
end
$$ language plpgsql;
ALTER FUNCTION databc.get_first_address(p_resourceinstanceid uuid) SECURITY DEFINER SET search_path = public;

drop function if exists databc.html_to_plain_string cascade;
create or replace function databc.html_to_plain_string(string_to_clean text) returns text as
$$
declare
begin
    return left(
            trim(
                    regexp_replace(
                            regexp_replace( -- <li> -> -
                                    regexp_replace( -- UL/LI to \n
                                            regexp_replace(string_to_clean, '<[/]{0,1}p>', '', 'gi')
                                        , '<ul><li>', E'\n- ', 'gi'),
                                    '<li>', '- ', 'gi'
                                ),
                            '(</ul>|</li>)', '', 'gi'
                        )), 4000);
end
$$ language plpgsql;
ALTER FUNCTION databc.html_to_plain_string(string_to_clean text) SECURITY DEFINER SET search_path = public;

drop function if exists databc.authority_priority cascade;
create or replace function databc.authority_priority(authority_level text) returns numeric as
$$
begin
    return
        case when authority_level = 'Provincial' then 2
            when authority_level = 'Municipal' then 1
            else 0 end;
end
$$ language plpgsql;

ALTER FUNCTION databc.authority_priority(authority_level text) SECURITY DEFINER SET search_path = public;


-- select * from MV_HISTORIC_ENVIRO_ONEROW_SITE order by borden_number;
-- select * from MV_HISTORIC_ENVIRO_ONEROW_SITE where borden_number in ('DcRu-235', 'DcRu-234');
-- select * from V_HISTORIC_ENVIRO_ONEROW_SITE where borden_number in ('DcRu-235', 'DcRu-234');

-- drop materialized view if exists MV_HISTORIC_ENVIRO_ONEROW_SITE;
-- refresh materialized view MV_HISTORIC_ENVIRO_ONEROW_SITE;
drop view if exists databc.V_HISTORIC_ENVIRO_ONEROW_SITE;
-- create materialized view MV_HISTORIC_ENVIRO_ONEROW_SITE as
create or replace view databc.V_HISTORIC_ENVIRO_ONEROW_SITE as
select distinct bn.resourceinstanceid site_id,
                bn.borden_number borden_number,
                case when br.officially_recognized_site then 'Y' else 'N' end is_officially_recognized,
                br.registration_status registration_status,
                cn.name                                 common_name,
                array_to_string(other_name.names, '; ') other_name,
                prop.pid         parcel_id,
                prop.street_address street_address,
                prop.city,
                prop.province,
                prop.locality,
                prop.location_description,
                br.authorities->>'government_name' government_name,
                br.authorities->>'authority' government_level,
                br.authorities->>'recognition_type' protection_type,
                to_date(br.authorities->>'start_date', 'YYYY-MM-DD') protection_start_date,
                br.authorities->>'reference_number' reference_number,
                case when mc.chronology is null then null else to_char(to_date(chronology[0]->>'start_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0) end construction_date,
                case when mc.chronology is not null and (chronology[0]->>'dates_approximate')::boolean then 'Circa' end construction_date_qualifier,
--                 case when mc.chronology is null then null else chronology[0]->>'event' end event_type,
--                 case when msra.crhp_submission_status = 'Approved' then 'Y' else 'N' end is_accepted_by_feds,
                case when significance_statement is null then null else (significance_statement->>'significance_type') end significance_type,
                case when significance_statement is null then null else (significance_statement->>'physical_description') end physical_description,
                case when significance_statement is null then null else (significance_statement->>'heritage_value') end heritage_value,
                case when significance_statement is null then null else (significance_statement->>'defining_elements') end defining_elements,
                case when significance_statement is null then null else (significance_statement->>'document_location') end document_location,
                ca.actors->>'Architect / Designer' architect_name,
                ca.actors->>'Builder' builder_name,
                hf.functional_states->>'Current' current_function,
                hf.functional_states->>'Historic' historic_function,
                msb.area_sqm::numeric(19,2) dimensions_area_sqm,
                msb.site_centroid_latitude::numeric(10,6) gis_latitude,
                msb.site_centroid_longitude::numeric(10,6) gis_longitude,
                msb.utmzone::numeric(2,0) utm_zone,
                msb.utmnorthing::numeric(10,0) utm_northing,
                msb.utmeasting::numeric(10,0) utm_easting,
                'https://apps.nrs.gov.bc.ca/int/bcrhp/report/'||bn.resourceinstanceid site_url,
                msb.site_boundary
--                 prop.location_description,
--                 prop.pin,
--                 prop.legal_description,
--                 msra.restricted,
--                ,msra.bcrhp_submission_status
--                 msra.date_submitted_to_crhp,
--                 msra.federal_id_number
from mv_borden_number bn
         left join (select resourceinstanceid, name from mv_site_names where name_type = 'Common') cn on cn.resourceinstanceid = bn.resourceinstanceid
         left join (select resourceinstanceid, array_agg(name) names from mv_site_names where name_type = 'Other' group by resourceinstanceid) other_name on other_name.resourceinstanceid = bn.resourceinstanceid
         join (select distinct r.resourceinstanceid,
                                    r.officially_recognized_site,
                                    r.registration_status,
                                    jsonb_agg(
                                            case when pe.authority is null then null else
                                                jsonb_build_object(
                                                        'authority', pe.authority,
                                                        'auth_order', databc.authority_priority(pe.authority),
                                                        'start_date', pe.designation_or_protection_start_date,
                                                        'government_name', pe.government_name,
                                                        'recognition_type', pe.recognition_type,
                                                        'reference_number', pe.reference_number
                                                    ) end order by databc.authority_priority(pe.authority) desc,
                                                designation_or_protection_start_date desc )->0 authorities
--                        pe.designation_or_protection_end_date, registry_types, pe.reference_number, pe.protection_notes, pe.legal_instrument, pe.act_section, pe.recognition_type, pe.government_type
                    from mv_bc_right r
                             left join mv_site_protection_event pe on r.bc_right_id = pe.bc_right_id
                    group by r.resourceinstanceid, r.officially_recognized_site, r.registration_status) br
                   on bn.resourceinstanceid = br.resourceinstanceid
         join mv_site_record_admin msra on bn.resourceinstanceid = msra.resourceinstanceid
         left join (select resourceinstanceid, jsonb_agg(
            jsonb_build_object(
                'start_year', start_year,
                'end_year', end_year,
                'dates_approximate', dates_approximate,
                'event', event,
                'source', source,
                'event_notes', event_notes) order by start_year
    ) chronology from mv_chronology where event = 'Construction' group by resourceinstanceid ) mc on bn.resourceinstanceid = mc.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_object_agg(state_period, array_to_string(functional_states, '; ') ) functional_states
                    from mv_heritage_function
                    group by resourceinstanceid) hf on bn.resourceinstanceid = hf.resourceinstanceid
         left join (select resourceinstanceid,
                           jsonb_object_agg(actor_type, array_to_string(actors, '; ')) actors
                    from mv_construction_actors
                    group by resourceinstanceid) ca on bn.resourceinstanceid = ca.resourceinstanceid
         left join mv_site_boundary msb on bn.resourceinstanceid = msb.resourceinstanceid
         left join (select resourceinstanceid,
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
                    from mv_bc_statement_of_significance group by resourceinstanceid) sos on bn.resourceinstanceid = sos.resourceinstanceid,
    databc.get_first_address(bn.resourceinstanceid) prop
where msra.bcrhp_submission_status in ('Approved - Basic Record','Approved - Full Record')
and registration_status in ('Federal Jurisdiction', 'Recorded/Unprotected', 'Registered', 'Legacy')
and not coalesce(msra.restricted, false);
