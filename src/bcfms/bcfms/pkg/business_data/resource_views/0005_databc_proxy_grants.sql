-- Schema databc and DataBC proxy object must be created prior to running this script
grant select on databc.important_fossil_areas_vw to {{ db_databc_user }};
grant select on databc.fossil_sites_vw to {{ db_databc_user }};
grant select on databc.provincially_protected_fossil_sites_vw to {{ db_databc_user }};
grant select on databc.collection_events_vw to {{ db_databc_user }};
