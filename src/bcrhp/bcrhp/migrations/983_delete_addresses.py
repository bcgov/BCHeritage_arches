from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bcrhp", "909_update_url_prefix"),
    ]

    backup_table_sql = """
        create table heritage_site.backup_983_bc_property_address as
        with borden_numbers as (select resourceinstanceid
                                from heritage_site.borden_number
                                where borden_number -> 'en' ->> 'value' in
                                      ('DiQh-68', 'DgQk-66', 'DgQk-69', 'FhRm-15', 'DjQh-20', 'FbRl-18'))
        select addr.*
        from borden_numbers bn
                 join (select pa.*
                       from heritage_site.bc_property_address pa
                                join heritage_site.bc_property_legal_description ld on ld.bc_property_address = pa.tileid
                       where ld.pid not in (9723528, 16025903, 13635531, 12825964, 5353891, 6047611)) addr
                      on addr.resourceinstanceid = bn.resourceinstanceid;

        create table heritage_site.backup_983_bc_property_legal_description as
        with borden_numbers as (select resourceinstanceid
                                from heritage_site.borden_number
                                where borden_number -> 'en' ->> 'value' in
                                      ('DiQh-68', 'DgQk-66', 'DgQk-69', 'FhRm-15', 'DjQh-20', 'FbRl-18'))
        select addr.*
        from borden_numbers bn
                 join (select ld.*
                       from heritage_site.bc_property_address pa
                                join heritage_site.bc_property_legal_description ld on ld.bc_property_address = pa.tileid
                       where ld.pid not in (9723528, 16025903, 13635531, 12825964, 5353891, 6047611)) addr
                      on addr.resourceinstanceid = bn.resourceinstanceid;
    """

    reverse_backup_table_sql = """
        drop table heritage_site.backup_983_bc_property_address;
        drop table heritage_site.backup_983_bc_property_legal_description;
    """

    sql = """
        begin;
        call __arches_prepare_bulk_load();
        DO
        $$
            DECLARE
                rows_to_delete cursor for
                    with all_rows as (select bn.resourceinstanceid                                site_uuid,
                                             add.address_uuid,
                                             pid                                                 ,
                                             add.legal_description_uuid
                                      from heritage_site.borden_number bn
                                               join (select pa.resourceinstanceid,
                                                            pa.tileid address_uuid,
                                                            ld.tileid legal_description_uuid,
                                                            ld.pid
                                                     from heritage_site.bc_property_address pa
                                                              join heritage_site.bc_property_legal_description ld
                                                                   on pa.tileid = ld.bc_property_address) add
                                                    on bn.resourceinstanceid = add.resourceinstanceid
                                      where borden_number -> 'en' ->> 'value' in
                                            ('DiQh-68', 'DgQk-66', 'DgQk-69', 'FhRm-15', 'DjQh-20', 'FbRl-18')
                                        and pid not in (9723528, 16025903, 13635531, 12825964, 5353891, 6047611)
                                      order by borden_number -> 'en' ->> 'value')
                    select array_agg(distinct address_uuid) address_uuids,
                           array_agg(distinct legal_description_uuid) legal_description_uuids
                    from all_rows addr_rows;

                ids_to_delete record;
                deleted_count integer;
            BEGIN

                open rows_to_delete;
                fetch rows_to_delete into ids_to_delete;
                close rows_to_delete;

                raise notice 'Number of addresses %', cardinality(ids_to_delete.address_uuids);
                raise notice 'Number of legal addresses %', cardinality(ids_to_delete.legal_description_UUIDs);

                delete
                from heritage_site.bc_property_legal_description
                where tileid = any (ids_to_delete.legal_description_UUIDs);
                GET DIAGNOSTICS deleted_count = ROW_COUNT;
                raise notice 'Deleted % legal description rows', deleted_count;
                delete
                from heritage_site.bc_property_address
                where tileid = any (ids_to_delete.address_uuids);
                GET DIAGNOSTICS deleted_count = ROW_COUNT;
                raise notice 'Deleted % address rows', deleted_count;
            end;
        $$ language 'plpgsql';
        commit;
        begin;
        call __arches_complete_bulk_load();
        commit;

    """

    reverse_sql = """
        begin;
        call __arches_prepare_bulk_load();
        insert into heritage_site.bc_property_address select * from heritage_site.backup_983_bc_property_address;
        insert into heritage_site.bc_property_legal_description select * from heritage_site.backup_983_bc_property_legal_description;
        commit;
        begin;
        call __arches_complete_bulk_load();
        select refresh_geojson_geometries();
        commit;
    """

    operations = [
        migrations.RunSQL(
            backup_table_sql,
            reverse_backup_table_sql,
        ),
        migrations.RunSQL(
            sql,
            reverse_sql,
        ),
    ]
