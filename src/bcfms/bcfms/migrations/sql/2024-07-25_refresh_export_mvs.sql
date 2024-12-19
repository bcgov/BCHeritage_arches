create or replace procedure refresh_export_mvs() as
$$
BEGIN
    refresh materialized view fossil_type.fossil_name_mv;
    refresh materialized view fossil_sample.fossil_name_mv;
    refresh materialized view fossil_sample.ce_sample_summary_mv;
    refresh materialized view publication.ce_publication_summary_mv;
END
$$ language plpgsql;
