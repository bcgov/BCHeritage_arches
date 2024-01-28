-- Schema databc and DataBC proxy object must be created prior to running this script
drop owned by proxy_databc cascade;
drop role proxy_databc;
create role proxy_databc password '{{ databc_api_password }}';
alter role proxy_databc with login;
alter role proxy_databc set search_path = databc;
revoke all on schema public from proxy_databc;
grant connect on database bcrhp to proxy_databc;
grant usage on schema databc to proxy_databc;
grant execute on function databc.get_first_address(p_resourceinstanceid uuid) to proxy_databc;
grant select on databc.V_HISTORIC_ENVIRO_ONEROW_SITE to proxy_databc;
