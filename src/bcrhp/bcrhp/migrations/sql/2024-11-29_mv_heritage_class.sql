create materialized view mv_heritage_class as
    select resourceinstanceid,
        jsonb_agg(
            jsonb_build_object(
                'resource_count', contributing_resource_count,
                'ownership', __arches_get_concept_label(ownership),
                'category', __arches_get_concept_label(heritage_category)
            )
        ) heritage_class
    from heritage_site.heritage_class group by resourceinstanceid;
create index mv_hc_idx on mv_heritage_class(resourceinstanceid);