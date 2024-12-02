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
