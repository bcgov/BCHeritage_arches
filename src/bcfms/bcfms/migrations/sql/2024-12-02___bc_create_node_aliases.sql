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