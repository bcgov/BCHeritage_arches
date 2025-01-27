create or replace procedure refresh_materialized_views() as
$$
BEGIN
    refresh materialized view mv_bc_right;
    refresh materialized view mv_bc_statement_of_significance;
    refresh materialized view mv_borden_number;
    refresh materialized view mv_chronology;
    refresh materialized view mv_construction_actors;
    refresh materialized view mv_government;
    refresh materialized view mv_heritage_function;
    refresh materialized view mv_heritage_class;
    refresh materialized view mv_heritage_theme;
    refresh materialized view mv_legal_description;
    refresh materialized view mv_property_address;
    refresh materialized view mv_unique_property_address;
    refresh materialized view mv_protection_event;
    refresh materialized view mv_geojson_geoms;
    refresh materialized view mv_site_boundary;
    refresh materialized view mv_site_names;
    refresh materialized view mv_site_protection_event;
    refresh materialized view mv_site_record_admin;
END
$$ language plpgsql;