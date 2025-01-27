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