drop view if exists fossil_collection_event.collection_event_csv_export_vw;
create or replace view fossil_collection_event.collection_event_csv_export_vw as
select
    row_uuid,
    collection_event_id,
    collection_start_year "Collection Start Year",
    location_descriptor "Location Descriptor",
    collection_location "Collection Location",
    storage_locations "Storage Locations",
    storage_references "Storage References",
    scientific_names "Scientific Names",
    common_names "Common Names",
    size_categories "Size Categories",
    geological_groups "Geological Groups",
    geological_formations "Geological Formations",
    geological_members "Geological Members",
    informal_names "Informal Name",
    other_names "Other Names",
    time_scale "Time Scale",
    minimum_time "Minumum Time",
    maximum_time "Maximum Time",
    publication_count "Publication Count",
    publication_years "Publication Year",
    publication_types  "Publication Type",
    authors  "Authors"
from fossil_collection_event.collection_event_vw
order by "Location Descriptor", "Collection Start Year";