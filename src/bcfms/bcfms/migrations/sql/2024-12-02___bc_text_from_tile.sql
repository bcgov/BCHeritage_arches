create or replace function __bc_text_from_tile(tiledata jsonb, nodeid uuid) returns text as
$$
DECLARE
BEGIN
    return tiledata[nodeid::text]->'en'->>'value';
END $$ language plpgsql;