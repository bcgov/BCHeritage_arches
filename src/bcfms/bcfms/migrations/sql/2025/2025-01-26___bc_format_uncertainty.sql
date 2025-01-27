CREATE OR REPLACE FUNCTION public.__bc_format_uncertainty(tiledata jsonb, nodeid uuid, uncertainty_nodeid uuid) RETURNS text
    LANGUAGE plpgsql
AS $$
DECLARE
    nodeval text;
    is_uncertain boolean;
BEGIN

    nodeval = __arches_get_node_display_value(tiledata, nodeid);
    if (nodeval is null or nodeval = '') then
        return '';
    else
        begin
            is_uncertain = (tiledata->uncertainty_nodeid::text) is not null and (tiledata->uncertainty_nodeid::text)::boolean;
        exception when others then
            is_uncertain = false;
            raise WARNING 'Unable to format as uncertainty: %', tiledata->>uncertainty_nodeid::text;
        end;
        return nodeval || (case when is_uncertain then ' ?' else '' end);
    end if;
END $$;

DO $$
    DECLARE
    BEGIN
        execute format('alter function public.__bc_format_uncertainty(jsonb, uuid, uuid) owner to %s;', current_database());
    END $$ language plpgsql;
