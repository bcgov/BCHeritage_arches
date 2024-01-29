-- Schema databc and DataBC proxy object must be created prior to running this script
grant execute on function databc.get_first_address(p_resourceinstanceid uuid) to {{ db_databc_user }};
grant select on databc.V_HISTORIC_ENVIRO_ONEROW_SITE to {{ db_databc_user }};
