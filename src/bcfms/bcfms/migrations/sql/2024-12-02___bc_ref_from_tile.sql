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