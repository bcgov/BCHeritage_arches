DO $$
    DECLARE
        update_rec record;
    BEGIN
        -- The pattern used so far is the app role name is the same as the database name. If this change, the logic for
        -- deriving the role name will need to change
        for update_rec in select * from pg_matviews  where matviewowner = 'postgres' order by matviewname loop
                execute format('alter materialized view %s owner to %s;', update_rec.schemaname||'.'||update_rec.matviewname, current_database());
            end loop;
        for update_rec in select * from pg_views
                          where schemaname not in ( 'information_schema', 'pg_catalog')
                            and viewname not in ('instances')
                            and viewowner = 'postgres'
                          order by schemaname, viewname loop
                execute format('alter view %s owner to %s;', update_rec.schemaname||'.'||update_rec.viewname, current_database());
            end loop;
    END $$ language plpgsql;