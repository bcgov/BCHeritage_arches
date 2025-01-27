create or replace function __bc_point_from_tile(tiledata jsonb, nodeid uuid) returns text as
$$
DECLARE
BEGIN
    return tiledata[nodeid::text]->'features'->0->'geometry'->>'coordinates';
END $$ language plpgsql;