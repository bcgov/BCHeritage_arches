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
