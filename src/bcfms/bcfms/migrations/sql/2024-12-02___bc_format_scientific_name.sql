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