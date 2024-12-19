create or replace view heritage_site.csv_export as
select
    resourceinstanceid as site_id
     , coalesce(borden_number, '') as "Borden Number"
     , coalesce(common_name, '') "Common Name"
     , coalesce(other_name, '') "Other Name"
     , coalesce(street_address, '') as "Street Address"
     , coalesce(city, '') as "City"
     , coalesce(locality, '') as "Locality"
     , coalesce(postal_code, '') as "Postal Code"
     , coalesce(location_description, '') as "Location Description"
     , coalesce(registration_status, '') as "Registration Status"
     , coalesce((
                    select string_agg(elem::text, '; ')
                    from jsonb_array_elements_text(authorities->'registry_types') as elem
                ), '') as "Registry Type"
     , coalesce(authorities->>'government_name', '') as "Recognition Government"
     , coalesce(authorities->>'recognition_type', '') as "Recognition Type"
     , coalesce(authorities->>'reference_number', '') as "Reference Number"
     , coalesce(to_char(to_date(authorities->>'start_date', 'YYYY-MM-DD'), 'YYYY-MM-DD'), '') as "Recognition Start Date"
     , coalesce(to_char(to_date(authorities->>'end_date', 'YYYY-MM-DD'), 'YYYY-MM-DD'), '') as "Recognition End Date"
     , coalesce(actors->'Architect / Designer'->>'actors', '') as "Architect/Designer"
     , coalesce(actors->'Builder'->>'actors', '') as "Builder"
     , concat(coalesce(actors->'Architect / Designer'->>'notes', ''),
              (case when actors->'Architect / Designer'->>'notes' <> '' and actors->'Builder'->>'notes' <> '' then '; ' else '' end),
              coalesce(actors->'Builder'->>'notes', ''))
    as "Architect/Builder Notes"
     , coalesce(chronology_data.chronology,'') as "Chronology"
     , coalesce(significance_statement->>'significance_type', '') as "SOS Type"
     , coalesce(significance_statement->>'physical_description', '') as "SOS Description"
     , coalesce(significance_statement->>'document_location', '') as "SOS Document Location"
     , coalesce(heritage_class, '') as "Heritage Class"
     , coalesce(functional_states->>'Current', '') as "Current Function"
     , coalesce(functional_states->>'Historic', '') as "Historic Function"
     , coalesce(heritage_theme, '') as "Heritage Theme"
from V_HISTORIC_SITE
         left join lateral (
    select
        string_agg(
                concat(
                        case when c.value->>'event' <> '' then concat(c.value->>'event', ' ')end,
                        case when (c.value->>'dates_approximate')::boolean then 'Circa ' end,
                        coalesce(to_char(to_date(c.value->>'start_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0)::text, ''), '-',
                        coalesce(to_char(to_date(c.value->>'end_year', 'YYYY-MM-DD'), 'YYYY')::numeric(4,0)::text, ''),
                        case when c.value->>'notes' <> '' then concat(': ', coalesce(c.value->>'notes', '-')) end
                    ), '; '
            ) as chronology
    from jsonb_array_elements(v_historic_site.chronology) as c(value)
    ) as chronology_data on true
order by "Borden Number";
DO
$$
    DECLARE
        app_user text;
    BEGIN
        select current_database() into app_user;
        EXECUTE format('grant select on heritage_site.csv_export to %s' ,quote_ident(app_user));
    end;
$$ language 'plpgsql';