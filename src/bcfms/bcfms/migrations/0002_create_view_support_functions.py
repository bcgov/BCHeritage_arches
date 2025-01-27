from django.db import migrations
from bcgov_arches_common.migrations.operations.privileged_sql import RunPrivilegedSQL


class Migration(migrations.Migration):
    dependencies = [('bcfms',
                     '0001_create_databc_proxy_role')]

    create_create_node_aliases = """
        create or replace procedure __bc_create_node_aliases(p_graph_slug text, p_schema_name text default null) as
        $$
        DECLARE
            node_rec record;
        BEGIN
            for node_rec in select n.* from nodes n join graphs g on n.graphid = g.graphid where g.slug = p_graph_slug loop
                      raise Notice '%', node_rec.alias;
                      execute format('create or replace function %I.%I() returns uuid as $body$ begin return ''%s''::uuid; end $body$ language plpgsql', coalesce(p_schema_name, p_graph_slug), node_rec.alias||'_nodeid', node_rec.nodeid);
                      execute format('create or replace function %I.%I() returns uuid as $body$ begin return ''%s''::uuid; end $body$ language plpgsql', coalesce(p_schema_name, p_graph_slug), node_rec.alias||'_nodegroupid', node_rec.nodegroupid);
                end loop;
        END $$ language plpgsql;
        """
    drop_create_node_aliases = """
        drop procedure if exists __bc_create_node_aliases;
        """

    create_text_from_tile = """
        create or replace function __bc_text_from_tile(tiledata jsonb, nodeid uuid) returns text as
        $$
        DECLARE
        BEGIN
            return tiledata[nodeid::text]->'en'->>'value';
        END $$ language plpgsql;
        """
    drop_text_from_tile = """
        drop function if exists __bc_text_from_tile;
        """

    create_point_from_tile = """
        create or replace function __bc_point_from_tile(tiledata jsonb, nodeid uuid) returns text as
        $$
        DECLARE
        BEGIN
            return tiledata[nodeid::text]->'features'->0->'geometry'->>'coordinates';
        END $$ language plpgsql;
        """
    drop_point_from_tile = """
        drop function if exists __bc_point_from_tile;
        """

    create_ref_from_tile = """
        create or replace function __bc_ref_from_tile(tiledata jsonb, nodeid uuid) returns setof uuid as
        $$
        DECLARE
        BEGIN
            if (jsonb_typeof(tiledata->(nodeid::text)) = 'null' or tiledata->>(nodeid::text)::text = '') then
                return query select null::uuid;
            else
                return query select (jsonb_array_elements(tiledata[nodeid::text])->>'resourceId')::uuid;
            end if;
        EXCEPTION WHEN OTHERS THEN
            raise EXCEPTION 'Unable to parse %', tiledata;
        END $$ language plpgsql;
        """

    drop_ref_from_tile = """
        drop function if exists __bc_ref_from_tile;
        """

    create_format_uncertainty = """
        create or replace function __bc_format_uncertainty(tiledata jsonb, nodeid uuid, uncertainty_nodeid uuid) returns text as
        $$
        DECLARE
            nodeval text;
            is_uncertain boolean;
        BEGIN

            nodeval = __arches_get_node_display_value(tiledata, nodeid);
            if (nodeval is null or nodeval = '') then
                return '';
            else
                is_uncertain = (tiledata->uncertainty_nodeid::text) is not null and (tiledata->uncertainty_nodeid::text)::boolean;
                return nodeval || (case when is_uncertain then ' ?' else '' end);
            end if;
        END $$ language plpgsql;
        """

    drop_format_uncertainty = """
        drop function if exists __bc_format_uncertainty;
        """

    create_unique_array = """
        create or replace function __bc_unique_array(p_inarray anyarray) returns anyarray as
        $$
        DECLARE
            uq_array text[];
        BEGIN
            with uq as (select distinct val from unnest(p_inarray) val
                                            where coalesce(val,'') <> '' order by 1)
            select array_agg(val) into uq_array from uq;
            return uq_array;
        END $$ language plpgsql;
        """
    drop_unique_array = """
        drop function if exists __bc_unique_array;
        """


    create_format_scientific_name = """
        create or replace function __bc_format_scientific_name(name text, name_rank text, connector text, other_name text, other_name_rank text) returns text as
        $$
        DECLARE
        BEGIN
            return trim(replace(coalesce(name, '') ||  ' ' ||
                                coalesce(connector, '') || ' ' ||
                                coalesce(other_name, '')
                , '  ', ' ')

                );
        END $$ language plpgsql;
        """

    drop_format_scientific_name = """
        drop function if exists __bc_format_scientific_name cascade;
        """

    operations = [
        RunPrivilegedSQL(create_create_node_aliases, drop_create_node_aliases),
        RunPrivilegedSQL(create_text_from_tile, drop_text_from_tile),
        RunPrivilegedSQL(create_point_from_tile, drop_point_from_tile),
        RunPrivilegedSQL(create_ref_from_tile, drop_ref_from_tile),
        RunPrivilegedSQL(create_format_uncertainty, drop_format_uncertainty),
        RunPrivilegedSQL(create_unique_array, drop_unique_array),
        RunPrivilegedSQL(create_format_scientific_name, drop_format_scientific_name),
    ]
