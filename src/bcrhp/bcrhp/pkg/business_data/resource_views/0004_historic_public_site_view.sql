drop view if exists databc.V_HISTORIC_ENVIRO_ONEROW_SITE;
drop view if exists heritage_site.csv_export;
drop view if exists V_HISTORIC_SITE;


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
    ca.actor_notes,
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
            (elm->>'ownership')::text || ' (' ||
            (elm->>'resource_count') || ')',
            ', '
        ) heritage_class
    from mv_heritage_class, jsonb_array_elements(heritage_class) elm
    group by resourceinstanceid
) hc on bn.resourceinstanceid = hc.resourceinstanceid
left join (select resourceinstanceid,
    jsonb_object_agg(
        actor_type, array_to_string(actors, '; ')
    ) actors,
    array_to_string(array_agg(notes), '; ') actor_notes
    from mv_construction_actors
    group by resourceinstanceid
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
) sos on bn.resourceinstanceid = sos.resourceinstanceid, databc.get_first_address(bn.resourceinstanceid) prop
;

create or replace view databc.V_HISTORIC_ENVIRO_ONEROW_SITE as
select
    resourceinstanceid site_id,
    borden_number borden_number,
    case when officially_recognized_site then 'Y' else 'N' end is_officially_recognized,
    registration_status registration_status,
    common_name,
    other_name,
    pid parcel_id,
    street_address,
    city,
    province,
    locality,
    location_description,
    authorities->>'government_name' government_name,
    authorities->>'authority' government_level,
    authorities->>'recognition_type' protection_type,
    to_date(authorities->>'start_date', 'YYYY-MM-DD') protection_start_date,
    authorities->>'reference_number' reference_number,
    case when chronology is null then null else to_char(to_date(chronology[0]->>'start_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0) end construction_date,
    case when chronology is not null and (chronology[0]->>'dates_approximate')::boolean then 'Circa' end construction_date_qualifier,
    case when significance_statement is null then null else (significance_statement->>'significance_type') end significance_type,
    case when significance_statement is null then null else (significance_statement->>'physical_description') end physical_description,
    case when significance_statement is null then null else (significance_statement->>'heritage_value') end heritage_value,
    case when significance_statement is null then null else (significance_statement->>'defining_elements') end defining_elements,
    case when significance_statement is null then null else (significance_statement->>'document_location') end document_location,
    actors->>'Architect / Designer' architect_name,
    actors->>'Builder' builder_name,
    functional_states->>'Current' current_function,
    functional_states->>'Historic' historic_function,
    dimensions_area_sqm,
    gis_latitude,
    gis_longitude,
    utm_zone,
    utm_northing,
    utm_easting,
    site_url,
    site_boundary
from V_HISTORIC_SITE
where bcrhp_submission_status in ('Approved - Basic Record','Approved - Full Record')
    and registration_status in ('Federal Jurisdiction', 'Recorded/Unprotected', 'Registered', 'Legacy')
-- FIXME: noticed that the original view only took from the first, and there can be multiples of these
--        need to investigate more
    and chronology->>'event' = 'Construction'
    and not coalesce(restricted, false)
;


create or replace view heritage_site.csv_export as
select
    borden_number as "Borden Number"
    , street_address as "Street Address"
    , city as "City"
    , locality as "Locality"
    , postal_code as "Postal Code"
    , location_description as "Location Description"
    , registration_status as "Registration Status"
    , authorities->>'registry_types' as "Registry Type"
    , authorities->>'government_name' as "Recognition Government"
    , authorities->>'recognition_type' as "Recognition Type"
    , authorities->>'reference_number' as "Reference Number"
    , to_date(authorities->>'start_date', 'YYYY-MM-DD') as "Recognition Start Date"
    , to_date(authorities->>'end_date', 'YYYY-MM-DD') as "Recognition End Date"
    , actors->>'Architect / Designer' as "Architect/Designer"
    , actors->>'Builder' as "Builder"
    , actor_notes as "Architect Builder Notes"
    , case when chronology is null then null else chronology[0]->>'event' end as "Chronology Event"
    , case when chronology is null then null else to_char(to_date(chronology[0]->>'start_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0) end as "Chronology Start Year"
    , case when chronology is null then null else to_char(to_date(chronology[0]->>'end_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0) end as "Chronology End Year"
    , case when chronology is null then null else chronology[0]->>'notes' end as "Chronology Notes"
    , case when significance_statement is null then null else (significance_statement->>'significance_type') end as "SOS Type"
    , case when significance_statement is null then null else (significance_statement->>'physical_description') end as "SOS Description"
    , case when significance_statement is null then null else (significance_statement->>'document_location') end as "SOS Document Location"
    , heritage_class as "Heritage Class"
    , functional_states->>'Current' as "Current Function"
    , functional_states->>'Historic' as "Historic Function"
    -- NOTE: it is the state_period
    -- Missing: , as "Function Period"
    , heritage_theme as "Heritage Theme"
from V_HISTORIC_SITE
;
