# Generated by Django 4.2.13 on 2024-07-05 09:19

from django.db import migrations
from django.db.migrations.operations import RunSQL
from bcrhp.migrations.operations.privileged_sql import RunPrivilegedSQL


class Migration(migrations.Migration):

    dependencies = [
        ('bcrhp', '694_3_set_initial_permissions'),
    ]

    operations = [
        RunSQL(
            """
            begin;
            update map_layers
            set legend = replace(legend, '/int/bcrhp/', '/bcrhp/')
            where legend like '%/int/bcrhp/%';
            commit;
            """,
            """
            begin;
            update map_layers
            set legend = replace(legend, '/bcrhp/', '/int/bcrhp/')
            where legend like '%/bcrhp/%';
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update map_sources
            set source = jsonb_set(
                source,
                '{tiles}',
                (
                    select jsonb_agg(to_jsonb(replace(value, '/int/bcrhp/', '/bcrhp/')))
                    from jsonb_array_elements_text(source -> 'tiles') as arr(value)
                )
            )
            where source::text like '%/int/bcrhp/%';
            commit;
            """,
            """
            begin;
            update map_sources
            set source = jsonb_set(
                source,
                '{tiles}',
                (
                    select jsonb_agg(to_jsonb(replace(value, '/bcrhp/', '/int/bcrhp/')))
                    from jsonb_array_elements_text(source -> 'tiles') as arr(value)
                )
            )
            where source::text like '%/bcrhp/%';
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update cards_x_nodes_x_widgets
            set config = jsonb_set(
                config,
                '{url}',
                ('"' || replace(config->>'url', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
            )
            where (config->'url') is not null
            and config->>'url' like '%/int/bcrhp/%';
            commit;
            """,
            """
            begin;
            update cards_x_nodes_x_widgets
            set config = jsonb_set(
                config,
                '{url}',
                ('"' || replace(config->>'url', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
            )
            where (config->'url') is not null
            and config->>'url' like '%/bcrhp/%';
            commit;
            """
        ),
        # dc12f414-0d07-11ed-8804-5254008afee6 - Site Document node
        # 0a883b80-2fb6-11ed-be5f-5254008afee6 - Site Image node (there are multiple but this uuid is the only one with results for the needed changes)
        RunSQL(
            """
            begin;
            -- for site documents
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{dc12f414-0d07-11ed-8804-5254008afee6}',
                jsonb_set(
                    (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6')::jsonb,
                    '{0, url}',
                    ('"' || replace((tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'url', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 -> 'url' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'url' like '%/int/bcrhp/%'
            ;
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{dc12f414-0d07-11ed-8804-5254008afee6}',
                jsonb_set(
                    (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6')::jsonb,
                    '{0, content}',
                    ('"' || replace((tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'content', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 -> 'content' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'content' like '%/int/bcrhp/%'
            ;
            -- for site images
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{0a883b80-2fb6-11ed-be5f-5254008afee6}',
                jsonb_set(
                    (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6')::jsonb,
                    '{0, url}',
                    ('"' || replace((tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'url', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 -> 'url' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'url' like '%/int/bcrhp/%'
            ;
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{0a883b80-2fb6-11ed-be5f-5254008afee6}',
                jsonb_set(
                    (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6')::jsonb,
                    '{0, content}',
                    ('"' || replace((tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'content', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 -> 'content' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'content' like '%/int/bcrhp/%'
            ;
            commit;
            """,
            """
            begin;
            -- for site documents
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{dc12f414-0d07-11ed-8804-5254008afee6}',
                jsonb_set(
                    (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6')::jsonb,
                    '{0, url}',
                    ('"' || replace((tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'url', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 -> 'url' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'url' like '%/bcrhp/%'
            ;
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{dc12f414-0d07-11ed-8804-5254008afee6}',
                jsonb_set(
                    (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6')::jsonb,
                    '{0, content}',
                    ('"' || replace((tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'content', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 -> 'content' is not null
            and (tiledata -> 'dc12f414-0d07-11ed-8804-5254008afee6') -> 0 ->> 'content' like '%/bcrhp/%'
            ;
            -- for site images
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{0a883b80-2fb6-11ed-be5f-5254008afee6}',
                jsonb_set(
                    (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6')::jsonb,
                    '{0, url}',
                    ('"' || replace((tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'url', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 -> 'url' is not null
            ;
            update tiles
            set tiledata = jsonb_set(
                tiledata,
                '{0a883b80-2fb6-11ed-be5f-5254008afee6}',
                jsonb_set(
                    (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6')::jsonb,
                    '{0, content}',
                    ('"' || replace((tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'content', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
                )
            )
            where tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 -> 'content' is not null
            and (tiledata -> '0a883b80-2fb6-11ed-be5f-5254008afee6') -> 0 ->> 'content' like '%/bcrhp/%'
            ;
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update nodes
            set config = jsonb_set(
                config,
                '{searchString}',
                ('"' || replace(config->>'searchString', '/int/bcrhp/', '/bcrhp/') || '"')::jsonb
            )
            where (config->'searchString') is not null
            and config->>'searchString' like '%/int/bcrhp/%'
            ;
            commit;
            """,
            """
            begin;
            update nodes
            set config = jsonb_set(
                config,
                '{searchString}',
                ('"' || replace(config->>'searchString', '/bcrhp/', '/int/bcrhp/') || '"')::jsonb
            )
            where (config->'searchString') is not null
            and config->>'searchString' like '%/bcrhp/%'
            ;
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update concepts
            set legacyoid = replace(legacyoid, '/int/bcrhp/', '/bcrhp/')
            where legacyoid like '%/int/bcrhp/%'
            ;
            commit;
            """,
            """
            begin;
            update concepts
            set legacyoid = replace(legacyoid, '/bcrhp/', '/int/bcrhp/')
            where legacyoid like '%/bcrhp/%'
            ;
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update values
            set value = replace(value, '/int/bcrhp/', '/bcrhp/')
            where value like '%/int/bcrhp/%'
            ;
            commit;
            """,
            """
            begin;
            update values
            set value = replace(value, '/bcrhp/', '/int/bcrhp/')
            where value like '%/bcrhp/%'
            ;
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update published_graphs
            set serialized_graph = replace(serialized_graph::text, '/int/bcrhp/', '/bcrhp/')::jsonb
            where serialized_graph::text like '%/int/bcrhp/%'
            ;
            commit;
            """,
            """
            begin;
            update published_graphs
            set serialized_graph = replace(serialized_graph::text, '/bcrhp/', '/int/bcrhp/')::jsonb
            where serialized_graph::text like '%/bcrhp/%'
            ;
            commit;
            """
        ),
        RunSQL(
            """
            begin;
            update edit_log
            set newvalue = replace(newvalue::text, '/int/bcrhp/', '/bcrhp/')::jsonb
            where newvalue::text like '%/int/bcrhp/';
            commit;
            """,
            """
            begin;
            update edit_log
            set newvalue = replace(newvalue::text, '/bcrhp/', '/int/bcrhp/')::jsonb
            where newvalue::text like '%/bcrhp/';
            commit;
            """
        ),
        RunPrivilegedSQL(
            """
            create or replace view V_HISTORIC_SITE as
            select distinct bn.resourceinstanceid,
                bn.borden_number,
                br.officially_recognized_site,
                br.registration_status registration_status,
                cn.name common_name,
                array_to_string(other_name.names, '; ') other_name,
                prop.pid,
                prop.street_address,
                prop.city,
                prop.postal_code,
                prop.province,
                prop.locality,
                prop.location_description,
                br.authorities,
                mc.chronology,
                significance_statement,
                ca.actors,
                hf.functional_states,
                ht.heritage_theme,
                hc.heritage_class,
                msb.area_sqm::numeric(19,2) dimensions_area_sqm,
                msb.site_centroid_latitude::numeric(10,6) gis_latitude,
                msb.site_centroid_longitude::numeric(10,6) gis_longitude,
                msb.utmzone::numeric(2,0) utm_zone,
                msb.utmnorthing::numeric(10,0) utm_northing,
                msb.utmeasting::numeric(10,0) utm_easting,
                'https://apps.nrs.gov.bc.ca/bcrhp/report/'||bn.resourceinstanceid site_url,
                msb.site_boundary,
                msra.bcrhp_submission_status,
                msra.restricted,
                msra.date_submitted_to_crhp
            from mv_borden_number bn
            left join (
                select resourceinstanceid, name
                from mv_site_names where name_type = 'Common'
            ) cn on cn.resourceinstanceid = bn.resourceinstanceid
            left join (
                select resourceinstanceid, array_agg(name) names
                from mv_site_names
                where name_type = 'Other'
                group by resourceinstanceid
            ) other_name on other_name.resourceinstanceid = bn.resourceinstanceid
            join (
                select distinct
                    r.resourceinstanceid,
                    r.officially_recognized_site,
                    r.registration_status,
                    jsonb_agg(
                        case when pe.authority is null then null else
                            jsonb_build_object(
                            'authority', pe.authority,
                            'auth_order', databc.authority_priority(pe.authority),
                            'start_date', pe.designation_or_protection_start_date,
                            'end_date', pe.designation_or_protection_end_date,
                            'government_name', pe.government_name,
                            'recognition_type', pe.recognition_type,
                            'reference_number', pe.reference_number,
                            'registry_types', r.registry_types
                        ) end order by databc.authority_priority(pe.authority) desc,
                        designation_or_protection_start_date desc
                    )->0 authorities
                from mv_bc_right r
                left join mv_site_protection_event pe on r.bc_right_id = pe.bc_right_id
                group by r.resourceinstanceid, r.officially_recognized_site, r.registration_status
            ) br on bn.resourceinstanceid = br.resourceinstanceid
            join mv_site_record_admin msra on bn.resourceinstanceid = msra.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_agg(
                        jsonb_build_object(
                        'start_year', start_year,
                        'end_year', end_year,
                        'dates_approximate', dates_approximate,
                        'event', event,
                        'source', source,
                        'event_notes', event_notes
                        ) order by start_year
                    ) chronology
                from mv_chronology
                group by resourceinstanceid
            ) mc on bn.resourceinstanceid = mc.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_object_agg(state_period, array_to_string(functional_states, '; ') ) functional_states
                from mv_heritage_function
                group by resourceinstanceid
            ) hf on bn.resourceinstanceid = hf.resourceinstanceid
            left join (
                select resourceinstanceid,
                    array_to_string(array_agg(heritage_theme), '; ') heritage_theme
                from mv_heritage_theme
                group by resourceinstanceid
            ) ht on bn.resourceinstanceid = ht.resourceinstanceid
            left join (
                select resourceinstanceid,
                    string_agg(
                        (elm->>'category')::text || ' ' ||
                        '(' || (elm->>'ownership')::text || ', ' ||
                        (elm->>'resource_count') || ')',
                        ', '
                    ) heritage_class
                from mv_heritage_class, jsonb_array_elements(heritage_class) elm
                group by resourceinstanceid
            ) hc on bn.resourceinstanceid = hc.resourceinstanceid
            left join (select resourceinstanceid,
                        jsonb_object_agg(
                                actor_type, jsonb_build_object('actors', array_to_string(actors, '; '), 'notes', array_to_string(notes, '; ') )
                            ) actors
                             from mv_construction_actors
                 group by resourceinstanceid order by resourceinstanceid
            ) ca on bn.resourceinstanceid = ca.resourceinstanceid
            left join mv_site_boundary msb on bn.resourceinstanceid = msb.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_agg(
                        jsonb_build_object(
                        'significance_type', databc.html_to_plain_string(significance_type),
                        'significance_level', databc.authority_priority(significance_type),
                        'physical_description', databc.html_to_plain_string(physical_description),
                        'defining_elements', databc.html_to_plain_string(defining_elements),
                        'heritage_value', databc.html_to_plain_string(heritage_value),
                        'document_location', databc.html_to_plain_string(document_location)
                        )
                        order by databc.authority_priority(significance_type) desc
                    )->0 significance_statement
                from mv_bc_statement_of_significance
                group by resourceinstanceid
            ) sos on bn.resourceinstanceid = sos.resourceinstanceid
            left join mv_unique_property_address prop on bn.resourceinstanceid = prop.resourceinstanceid;
            """,
            """
            create or replace view V_HISTORIC_SITE as
            select distinct bn.resourceinstanceid,
                bn.borden_number,
                br.officially_recognized_site,
                br.registration_status registration_status,
                cn.name common_name,
                array_to_string(other_name.names, '; ') other_name,
                prop.pid,
                prop.street_address,
                prop.city,
                prop.postal_code,
                prop.province,
                prop.locality,
                prop.location_description,
                br.authorities,
                mc.chronology,
                significance_statement,
                ca.actors,
                hf.functional_states,
                ht.heritage_theme,
                hc.heritage_class,
                msb.area_sqm::numeric(19,2) dimensions_area_sqm,
                msb.site_centroid_latitude::numeric(10,6) gis_latitude,
                msb.site_centroid_longitude::numeric(10,6) gis_longitude,
                msb.utmzone::numeric(2,0) utm_zone,
                msb.utmnorthing::numeric(10,0) utm_northing,
                msb.utmeasting::numeric(10,0) utm_easting,
                'https://apps.nrs.gov.bc.ca/int/bcrhp/report/'||bn.resourceinstanceid site_url,
                msb.site_boundary,
                msra.bcrhp_submission_status,
                msra.restricted,
                msra.date_submitted_to_crhp
            from mv_borden_number bn
            left join (
                select resourceinstanceid, name
                from mv_site_names where name_type = 'Common'
            ) cn on cn.resourceinstanceid = bn.resourceinstanceid
            left join (
                select resourceinstanceid, array_agg(name) names
                from mv_site_names
                where name_type = 'Other'
                group by resourceinstanceid
            ) other_name on other_name.resourceinstanceid = bn.resourceinstanceid
            join (
                select distinct
                    r.resourceinstanceid,
                    r.officially_recognized_site,
                    r.registration_status,
                    jsonb_agg(
                        case when pe.authority is null then null else
                            jsonb_build_object(
                            'authority', pe.authority,
                            'auth_order', databc.authority_priority(pe.authority),
                            'start_date', pe.designation_or_protection_start_date,
                            'end_date', pe.designation_or_protection_end_date,
                            'government_name', pe.government_name,
                            'recognition_type', pe.recognition_type,
                            'reference_number', pe.reference_number,
                            'registry_types', r.registry_types
                        ) end order by databc.authority_priority(pe.authority) desc,
                        designation_or_protection_start_date desc
                    )->0 authorities
                from mv_bc_right r
                left join mv_site_protection_event pe on r.bc_right_id = pe.bc_right_id
                group by r.resourceinstanceid, r.officially_recognized_site, r.registration_status
            ) br on bn.resourceinstanceid = br.resourceinstanceid
            join mv_site_record_admin msra on bn.resourceinstanceid = msra.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_agg(
                        jsonb_build_object(
                        'start_year', start_year,
                        'end_year', end_year,
                        'dates_approximate', dates_approximate,
                        'event', event,
                        'source', source,
                        'event_notes', event_notes
                        ) order by start_year
                    ) chronology
                from mv_chronology
                group by resourceinstanceid
            ) mc on bn.resourceinstanceid = mc.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_object_agg(state_period, array_to_string(functional_states, '; ') ) functional_states
                from mv_heritage_function
                group by resourceinstanceid
            ) hf on bn.resourceinstanceid = hf.resourceinstanceid
            left join (
                select resourceinstanceid,
                    array_to_string(array_agg(heritage_theme), '; ') heritage_theme
                from mv_heritage_theme
                group by resourceinstanceid
            ) ht on bn.resourceinstanceid = ht.resourceinstanceid
            left join (
                select resourceinstanceid,
                    string_agg(
                        (elm->>'category')::text || ' ' ||
                        '(' || (elm->>'ownership')::text || ', ' ||
                        (elm->>'resource_count') || ')',
                        ', '
                    ) heritage_class
                from mv_heritage_class, jsonb_array_elements(heritage_class) elm
                group by resourceinstanceid
            ) hc on bn.resourceinstanceid = hc.resourceinstanceid
            left join (select resourceinstanceid,
                        jsonb_object_agg(
                                actor_type, jsonb_build_object('actors', array_to_string(actors, '; '), 'notes', array_to_string(notes, '; ') )
                            ) actors
                             from mv_construction_actors
                 group by resourceinstanceid order by resourceinstanceid
            ) ca on bn.resourceinstanceid = ca.resourceinstanceid
            left join mv_site_boundary msb on bn.resourceinstanceid = msb.resourceinstanceid
            left join (
                select resourceinstanceid,
                    jsonb_agg(
                        jsonb_build_object(
                        'significance_type', databc.html_to_plain_string(significance_type),
                        'significance_level', databc.authority_priority(significance_type),
                        'physical_description', databc.html_to_plain_string(physical_description),
                        'defining_elements', databc.html_to_plain_string(defining_elements),
                        'heritage_value', databc.html_to_plain_string(heritage_value),
                        'document_location', databc.html_to_plain_string(document_location)
                        )
                        order by databc.authority_priority(significance_type) desc
                    )->0 significance_statement
                from mv_bc_statement_of_significance
                group by resourceinstanceid
            ) sos on bn.resourceinstanceid = sos.resourceinstanceid
            left join mv_unique_property_address prop on bn.resourceinstanceid = prop.resourceinstanceid;
            """
        )
    ]