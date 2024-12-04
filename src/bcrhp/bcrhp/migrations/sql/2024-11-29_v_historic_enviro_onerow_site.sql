create or replace view databc.V_HISTORIC_ENVIRO_ONEROW_SITE as
select distinct
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
    case when chronology is null then null else
        (select
             to_char(to_date(a->>'start_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0)
         from jsonb_array_elements(chronology) a where a->>'event' = 'Construction' limit 1)
        end construction_date,
    case when chronology is null then null else
        (select case when (a->>'dates_approximate')::boolean then 'Circa' end
         from jsonb_array_elements(chronology) a where a->>'event' = 'Construction' limit 1)
        end construction_date_qualifier,               case when significance_statement is null then null else (significance_statement->>'significance_type') end significance_type,
    case when significance_statement is null then null else (significance_statement->>'physical_description') end physical_description,
    case when significance_statement is null then null else (significance_statement->>'heritage_value') end heritage_value,
    case when significance_statement is null then null else (significance_statement->>'defining_elements') end defining_elements,
    case when significance_statement is null then null else (significance_statement->>'document_location') end document_location,
    actors->'Architect / Designer'->>'actors' architect_name,
    actors->'Builder'->>'actors'  builder_name,
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
  and not coalesce(restricted, false);
DO
$$
    DECLARE
        databc_user text;
    BEGIN
        select replace(current_database(), 'bcrhp','proxy_databc') into databc_user;
        EXECUTE format('grant select on databc.v_historic_enviro_onerow_site to %s' ,quote_ident(databc_user));
    end;
$$ language 'plpgsql';