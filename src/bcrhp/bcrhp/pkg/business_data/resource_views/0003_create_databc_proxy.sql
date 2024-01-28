-- Schema databc and DataBC proxy object must be created prior to running this script
DO
$$
    DECLARE
        databc_role record;
    BEGIN
        for databc_role in (select rolname from pg_roles where rolname = '{{ db_databc_user }}') loop
            Raise NOTICE 'Dropping role {{  db_databc_user }} and all associated grants';
            drop owned by {{ db_databc_user }} cascade;
            drop role {{ db_databc_user }};
        end loop;
    END
$$ language plpgsql;

create role {{ db_databc_user }} password '{{ databc_api_password }}';
alter role {{ db_databc_user }} with login;
alter role {{ db_databc_user }} set search_path = databc;
revoke all on schema public from {{ db_databc_user }};
grant connect on database bcrhp to {{ db_databc_user }};
grant usage on schema databc to {{ db_databc_user }};
grant execute on function databc.get_first_address(p_resourceinstanceid uuid) to {{ db_databc_user }};
grant select on databc.V_HISTORIC_ENVIRO_ONEROW_SITE to {{ db_databc_user }};
