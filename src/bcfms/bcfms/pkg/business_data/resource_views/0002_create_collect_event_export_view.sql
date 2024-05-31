-- drop materialized view fossil_collection_event.collection_details_mv;
-- create materialized view fossil_collection_event.collection_details_mv as
--     select resourceinstanceid,
--            tileid collection_details_uuid,
--            collection_start_year,
--            field_notes->'en'->>'value' field_notes
-- from fossil_collection_event.collection_details;
-- create index cd_idx1 on fossil_collection_event.collection_details_mv(collection_details_uuid);
-- create index cd_idx2 on fossil_collection_event.collection_details_mv(resourceinstanceid);
--
-- drop materialized view if exists fossil_collection_event.collection_event_location_mv;
-- create materialized view fossil_collection_event.collection_event_location_mv as
-- select resourceinstanceid,
--        collection_details,
--        location_descriptor->'en'->>'value' location_descriptor,
--        detailed_location->'en'->>'value' detailed_location,
--        st_asgeojson(collection_location)::jsonb->'coordinates'->0 collection_location
-- from fossil_collection_event.collection_event_location;
-- create index cel_idx1 on fossil_collection_event.collection_event_location_mv(resourceinstanceid);
-- create index cel_idx2 on fossil_collection_event.collection_event_location_mv(collection_details);
--
-- drop materialized view if exists fossil_collection_event.samples_collected_mv;
-- create materialized view fossil_collection_event.samples_collected_mv as
-- select resourceinstanceid,
--        (jsonb_array_elements(samples_collected)->>'resourceId')::uuid sample_uuid
-- from fossil_collection_event.samples_collected;
-- create index sc_idx1 on fossil_collection_event.samples_collected_mv(resourceinstanceid);
--
--
-- drop view if exists fossil_collection_event.collection_event_vw;
-- -- create or replace view fossil_collection_event.collection_event_vw as
-- select cd.resourceinstanceid collection_event_uuid,
--        cd.collection_start_year,
--        cel.location_descriptor,
--        cel.collection_location,
--        sc.sample_uuid
-- --         ,*
-- from fossil_collection_event.collection_details_mv cd
--            left join fossil_collection_event.collection_event_location_mv cel on cd.collection_details_uuid = cel.collection_details
--            left join fossil_collection_event.samples_collected_mv sc on cd.resourceinstanceid = sc.resourceinstanceid;

-- drop function __bc_node_id_for_alias;
-- create or replace function __bc_node_id_for_alias(p_alias text, p_graph_slug text default null) returns uuid as
--     $$
-- DECLARE
--     l_nodeid uuid;
-- BEGIN
--     select nodeid
--     into l_nodeid
--     from nodes
--              join graphs g on nodes.graphid = g.graphid
--     where alias = p_alias
--       and g.slug = coalesce(p_graph_slug, g.slug);
--     return l_nodeid;
-- END $$ language plpgsql;
--
-- drop function __bc_nodegroup_id_for_alias;
-- create or replace function __bc_nodegroup_id_for_alias(p_alias text, p_graph_slug text default null) returns uuid as
-- $$
-- DECLARE
--     l_nodeid uuid;
-- BEGIN
--     select nodegroupid
--     into l_nodeid
--     from nodes
--              join graphs g on nodes.graphid = g.graphid
--     where alias = p_alias
--       and g.slug = coalesce(p_graph_slug, g.slug);
--     return l_nodeid;
-- END $$ language plpgsql;

drop procedure if exists __bc_create_node_aliases;
create or replace procedure __bc_create_node_aliases(p_graph_slug text, p_schema_name text default null) as
$$
DECLARE
    node_rec record;
BEGIN
    for node_rec in select n.* from nodes n join graphs g on n.graphid = g.graphid where g.slug = p_graph_slug loop
              raise Notice '%', node_rec.alias;
              execute format('create or replace function %I.%I() returns uuid as $body$ begin return ''%s''::uuid; end $body$ language plpgsql', coalesce(p_schema_name, p_graph_slug), node_rec.alias||'_nodeid', node_rec.nodeid);
              execute format('create or replace function %I.%I() returns uuid as $body$ begin return ''%s''::uuid; end $body$ language plpgsql', coalesce(p_schema_name, p_graph_slug), node_rec.alias||'_nodegroupid', node_rec.nodegroupid);
        end loop;
END $$ language plpgsql;

drop function if exists __bc_text_from_tile;
create or replace function __bc_text_from_tile(tiledata jsonb, nodeid uuid) returns text as
$$
DECLARE
BEGIN
    return tiledata[nodeid::text]->'en'->>'value';
END $$ language plpgsql;

drop function if exists __bc_point_from_tile;
create or replace function __bc_point_from_tile(tiledata jsonb, nodeid uuid) returns text as
$$
DECLARE
BEGIN
    return tiledata[nodeid::text]->'features'->0->'geometry'->>'coordinates';
END $$ language plpgsql;

drop function if exists __bc_ref_from_tile;
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

drop function if exists __bc_format_uncertainty;
create or replace function __bc_format_uncertainty(tiledata jsonb, nodeid uuid, uncertainty_nodeid uuid) returns text as
$$
DECLARE
    nodeval text;
    is_uncertain boolean;
BEGIN

    nodeval = __arches_get_node_display_value(tiledata, nodeid);
    if (nodeval is null or nodeval = '') then
        return '';
    else
        is_uncertain = (tiledata->uncertainty_nodeid::text) is not null and (tiledata->uncertainty_nodeid::text)::boolean;
        return nodeval || (case when is_uncertain then ' ?' else '' end);
    end if;
END $$ language plpgsql;

drop function if exists __bc_unique_array;
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

/*
 * Format the scientific name parts (name, connector other name) into a string
 */
drop function if exists __bc_format_scientific_name cascade;
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

-- with repo_info as (select resourceinstanceid,
--                           __bc_ref_from_tile(tiledata, fossil_sample.repository_name_nodeid()) repository_uuid,
--                           __bc_text_from_tile(tiledata, fossil_sample.storage_reference_nodeid()) "Storage Reference"
--                    from tiles where nodegroupid = fossil_sample.repository_information_nodegroupid())
-- select ri.*
--        ,sl.storage_location_name->'en'->>'value' "Storage Location Name"
-- from repo_info ri
--          left join fossil_storage_location.storage_location_identifier sl
--                    on ri.repository_uuid = sl.resourceinstanceid
-- order by "Storage Location Name";
-- -- where ri.resourceinstanceid = '30e19a47-c255-4a6c-b3a4-0f778315dae9'::uuid;


call __bc_create_node_aliases('collection_event', 'fossil_collection_event');
call __bc_create_node_aliases('fossil_sample');
call __bc_create_node_aliases('fossil_type');
call __bc_create_node_aliases('storage_location','fossil_storage_location');
call __bc_create_node_aliases('publication');
call __bc_create_node_aliases('contributor');


drop view if exists fossil_sample.fossil_name_vw;
create or replace view fossil_sample.fossil_name_vw as
select
    resourceinstanceid fossil_sample_uuid,
    __bc_ref_from_tile(tiledata, fossil_sample.scientific_name_nodeid()) scientific_name,
    __arches_get_node_display_value(tiledata, fossil_sample.open_nomanclature_term_nodeid()) name_connector,
    __bc_ref_from_tile(tiledata, fossil_sample.other_scientific_name_nodeid()) other_scientific_name,
    __bc_ref_from_tile(tiledata, fossil_sample.fossil_common_name_nodeid()) common_name,
    __arches_get_node_display_value(tiledata, fossil_sample.fossil_size_category_v_nodeid()) size_category
from tiles where nodegroupid = fossil_sample.bc_fossil_identification_nodegroupid();
-- select * from fossil_sample.fossil_name_vw;

create materialized view fossil_sample.mv_fossil_name as select * from fossil_sample.fossil_name_vw;
create index fs_fnmv_idx1 on fossil_sample.mv_fossil_name(fossil_sample_uuid);
create index fs_fnmv_idx2 on fossil_sample.mv_fossil_name(scientific_name, other_scientific_name, common_name);


drop view if exists fossil_sample.storage_location_vw cascade;
create or replace view fossil_sample.storage_location_vw as
select sri.*,
       ri.location_name storage_location_name
from (select resourceinstanceid collected_sample_uuid,
             __bc_ref_from_tile(tiledata, fossil_sample.repository_name_nodeid()) repository_uuid,
             __bc_text_from_tile(tiledata, fossil_sample.storage_reference_nodeid()) storage_reference
      from tiles where nodegroupid = fossil_sample.repository_information_nodegroupid()) sri
         left join (select resourceinstanceid,
                           __bc_text_from_tile(tiledata, fossil_storage_location.storage_location_name_nodeid()) location_name
                    from tiles where nodegroupid = fossil_storage_location.storage_location_name_nodegroupid()) ri on sri.repository_uuid = ri.resourceinstanceid;


drop view if exists fossil_sample.stratigraphy_vw;
create or replace view fossil_sample.stratigraphy_vw as
select resourceinstanceid                                                                          fossil_sample_uuid,

       __bc_format_uncertainty(tiledata, fossil_sample.geological_group_nodeid(),
                               fossil_sample.geological_group_uncertain_nodeid())                  geological_group,
       __bc_format_uncertainty(tiledata, fossil_sample.geological_formation_nodeid(),
                               fossil_sample.geological_formation_uncertain_nodeid())              geological_formation,
       __bc_format_uncertainty(tiledata, fossil_sample.geological_member_nodeid(),
                               fossil_sample.geological_member_uncertain_nodeid())                 geological_member,
       __arches_get_node_display_value(tiledata, fossil_sample.informal_map_unit_or_name_nodeid()) informal_name,
       __bc_text_from_tile(tiledata, fossil_sample.other_stratigraphic_name_nodeid())              other_name
from tiles
where nodegroupid = fossil_sample.stratigraphy_nodegroupid();
-- select * from fossil_sample.storage_location_vw;

drop view if exists fossil_sample.geological_age_vw cascade;
create or replace view fossil_sample.geological_age_vw as
select resourceinstanceid                                                                          fossil_sample_uuid,
       __arches_get_node_display_value(tiledata, fossil_sample.geologic_timescale_division_nodeid()) time_scale,
       __bc_format_uncertainty(tiledata, fossil_sample.minimum_time_nodeid(),
                               fossil_sample.minimum_time_uncertain_nodeid())                  minimum_time,
       __bc_format_uncertainty(tiledata, fossil_sample.maximum_time_nodeid(),
                               fossil_sample.maximum_time_uncertain_nodeid())              maximum_time
from tiles
where nodegroupid = fossil_sample.geological_age_nodegroupid();
-- select * from fossil_sample.geological_age_vw;

drop view if exists fossil_type.fossil_name_vw cascade;
create view fossil_type.fossil_name_vw as
with name_qry as
         (select
              resourceinstanceid,
              tileid,
              __bc_text_from_tile(tiledata, fossil_Type.name_nodeid()) name,
              __bc_ref_from_tile(tiledata, fossil_type.parent_name_nodeid()) parent_name,
              __arches_get_node_display_value(tiledata, fossil_type.name_type_nodeid()) name_type,
              __arches_get_node_display_value(tiledata, fossil_type.taxonomic_rank_nodeid()) taxonomic_rank
          from tiles where nodegroupid = fossil_type.name_nodegroupid())
select distinct  child.resourceinstanceid fossil_name_uuid,
--        parent.tileid parent_tile,
--        child.tileid child_tile,
                 trim(coalesce(parent.name, '') || ' ' || coalesce(child.name,'') || case when coalesce(child.taxonomic_rank, parent.taxonomic_rank) = 'Genus' then ' sp.' else '' end) name,
--        parent.name parent_name,
--        child.name child_name,
--        child.parent_name,
                 coalesce(child.name_type, parent.name_type) name_type,
                 coalesce(child.taxonomic_rank, parent.taxonomic_rank) taxonomic_rank
from name_qry child
         left join name_qry parent on child.parent_name::uuid = parent.resourceinstanceid
order by trim(coalesce(parent.name, '') || ' ' || coalesce(child.name,'') || case when coalesce(child.taxonomic_rank, parent.taxonomic_rank) = 'Genus' then ' sp.' else '' end);

create materialized view fossil_type.mv_fossil_name as select * from fossil_type.fossil_name_vw;
create index ft_fn_mv_idx1 on fossil_type.mv_fossil_name(fossil_name_uuid);

/*
 * Materialized view that summarizes all the fossil samples associated with a collection event
 */
drop materialized view if exists fossil_sample.mv_ce_sample_summary;
create materialized view fossil_sample.mv_ce_sample_summary as
with ce_samples_collected as (select resourceinstanceid collection_event_id,
                                     __bc_ref_from_tile(tiledata,
                                                        fossil_collection_event.samples_collected_nodeid()) samples_collected_uuid
                              from tiles
                              where nodegroupid = fossil_collection_event.samples_collected_nodegroupid())
select coll.collection_event_id,
       count(*) samples_collected,
       array_to_string(array_remove(array_agg(distinct slv.storage_location_name order by storage_location_name), null), '; ') storage_locations,
       array_to_string(array_remove(array_agg(distinct slv.storage_reference order by storage_reference), null), '; ') storage_references,
       array_to_string(array_remove(array_agg(distinct __bc_format_scientific_name(s1.name, s1.taxonomic_rank, s.name_connector, s2.name, s2.taxonomic_rank)
                                              order by __bc_format_scientific_name(s1.name, s1.taxonomic_rank, s.name_connector, s2.name, s2.taxonomic_rank)), ''),'; ') scientific_names,
       array_to_string(array_remove(array_agg(distinct cn.name order by cn.name),null), '; ') common_names,
       array_to_string(array_remove(array_agg(distinct s.size_category order by s.size_category), null), '; ') size_categories,
       array_to_string(array_remove(array_agg(distinct geological_group), ''), '; ') geological_groups,
       array_to_string(array_remove(array_agg(distinct geological_formation), ''), '; ') geological_formations,
       array_to_string(array_remove(array_agg(distinct geological_member), ''), '; ') geological_members,
       array_to_string(array_remove(array_agg(distinct informal_name), ''), '; ') informal_names,
       array_to_string(array_remove(array_agg(distinct other_name), ''), '; ') other_names,
       min(time_scale) time_scale,  -- Geological Age is a 1:1 with fossil sample, so just use the min values
       min(minimum_time) minimum_time,
       min(maximum_time) maximum_time
from ce_samples_collected coll
         left join fossil_sample.geological_age_vw ga on coll.samples_collected_uuid = ga.fossil_sample_uuid
         left join fossil_sample.stratigraphy_vw strat on coll.samples_collected_uuid = strat.fossil_sample_uuid,
     fossil_sample.mv_fossil_name s
         left join fossil_type.mv_fossil_name s1 on s.scientific_name = s1.fossil_name_uuid
         left join fossil_type.mv_fossil_name s2 on s.other_scientific_name = s2.fossil_name_uuid
         left join fossil_type.mv_fossil_name cn on s.common_name = cn.fossil_name_uuid
         left join fossil_sample.storage_location_vw slv on s.fossil_sample_uuid = slv.collected_sample_uuid
where coll.samples_collected_uuid = s.fossil_sample_uuid
group by coll.collection_event_id;
create unique index ce_sample_summary_idx1 on fossil_sample.mv_ce_sample_summary(collection_event_id);
-- select * from fossil_type.fossil_name_vw;


drop view if exists publication.publication_details_vw;
create or replace view publication.publication_details_vw as
with publication_details as (
select
    resourceinstanceid publication_uuid,
    __arches_get_node_display_value(tiledata, publication.year_of_publication_nodeid()) publication_year,
    __bc_text_from_tile(tiledata, publication.title_nodeid()) title,
    __arches_get_node_display_value(tiledata, publication.publication_type_nodeid()) publication_type,
    __bc_ref_from_tile(tiledata, publication.journal_or_volume_name_nodeid()) parent_publication
from tiles where nodegroupid = publication.publication_details_nodegroupid()),
    publication_references as (
        select
            resourceinstanceid publication_uuid,
            __bc_ref_from_tile(tiledata, publication.collection_events_nodeid()) collection_event,
            __bc_ref_from_tile(tiledata, publication.fossil_samples_nodeid()) fossil_sample,
            __bc_ref_from_tile(tiledata, publication.fossil_types_nodeid()) fossil_type,
            __bc_ref_from_tile(tiledata, publication.fossil_sites_nodeid()) fossil_site,
            __bc_ref_from_tile(tiledata, publication.repositories_nodeid()) repository
        from tiles where nodegroupid = publication.reference_link_nodegroupid()),
    publication_authors as (
        select
            resourceinstanceid publication_uuid,
            __bc_ref_from_tile(tiledata, publication.authors_nodeid()) author_uuid
        from tiles where nodegroupid = publication.authors_nodegroupid()
    ),
    contributors as (
        select
            resourceinstanceid contributor_uuid,
            __bc_text_from_tile(tiledata, contributor.contributor_name_nodeid()) contributor_name,
            __bc_text_from_tile(tiledata, contributor.first_name_nodeid()) first_name,
            __arches_get_node_display_value(tiledata, contributor.contributor_type_nodeid()) contributor_type,
            __arches_get_node_display_value(tiledata, contributor.contributor_role_nodeid()) contributor_role
        from tiles where nodegroupid = contributor.contributor_nodeid()
    )
select pd.publication_uuid,
    pp.journal_title,
    pd.title,
    pd.publication_year,
    pd.publication_type,
    pa.contributor_name || case when pa.first_name is not null then ', '||pa.first_name else '' end author_name,
    pa.contributor_type,
    pa.contributor_role,
    pr.fossil_site,
    pr.collection_event,
    pr.fossil_sample,
    pr.fossil_type,
    pr.repository
from publication_details pd
    left join publication_references pr on pd.publication_uuid = pr.publication_uuid
    left join (select * from publication_authors a join contributors c on a.author_uuid = c.contributor_uuid)
        pa on pd.publication_uuid = pa.publication_uuid
    left join (select volume.publication_uuid, coalesce(journal.title, '') || ' ' || coalesce(volume.title, '') journal_title, volume.publication_type
               from publication_details volume
        left join publication_details journal on journal.publication_uuid = volume.parent_publication
                        where volume.publication_type = 'Volume / Publication Number'
                        ) pp on pp.publication_uuid = pd.parent_publication;

drop materialized view publication.mv_ce_publication_summary cascade;
create materialized view publication.mv_ce_publication_summary as
select collection_event,
       array_to_string(array_agg(distinct publication_year order by publication_year), '; ') publication_years,
       array_to_string(array_agg(distinct publication_type order by publication_type),'; ') publication_types,
       array_to_string(array_agg(distinct author_name order by author_name), '; ') authors,
       count(distinct publication_uuid) publication_count
from publication.publication_details_vw
group by collection_event
order by collection_event;
create unique index ce_ps_idx1 on publication.mv_ce_publication_summary(collection_event);


drop view if exists fossil_collection_event.collection_event_vw;
create or replace view fossil_collection_event.collection_event_vw as
with ce_collection_details as (select * from tiles where nodegroupid = fossil_collection_event.collection_start_year_nodegroupid()),
     ce_location as (select * from tiles where nodegroupid = fossil_collection_event.collection_location_nodegroupid()), /*__bc_nodegroup_id_for_alias('collection_location', 'collection_event')*/--
     ce_samples_collected as (select resourceinstanceid,
                                     __bc_ref_from_tile(tiledata,
                                                        fossil_collection_event.samples_collected_nodeid()) samples_collected_uuid
                              from tiles
                              where nodegroupid = fossil_collection_event.samples_collected_nodegroupid())--,
select
    uuid_generate_v4() row_uuid,
    ced.resourceinstanceid collection_event_id,
    coalesce(__arches_get_node_display_value(ced.tiledata, fossil_collection_event.collection_start_year_nodeid()), '') "Collection Start Year",
    __bc_text_from_tile(cel.tiledata, fossil_collection_event.location_descriptor_nodeid()) "Location Descriptor",
    __bc_point_from_tile(cel.tiledata, fossil_collection_event.collection_location_nodeid()) "Collection Location",
--     st_asgeojson(cel.tiledata->>'collection_location')::jsonb->'coordinates'->0 "Collection Location",
--     __arches_get_node_display_value(cel.tiledata, fossil_collection_event.collection_location_nodeid()),
--     cesc.samples_collected_uuid,
    ce_sample_summary.storage_locations "Storage Locations",
    ce_sample_summary.storage_references "Storage References",
    ce_sample_summary.scientific_names "Scientific Names",
    ce_sample_summary.common_names "Common Names",
    ce_sample_summary.size_categories "Size Categories",
    ce_sample_summary.geological_groups "Geological Groups",
    ce_sample_summary.geological_formations "Geological Formations",
    ce_sample_summary.geological_members "Geological Members",
    ce_sample_summary.informal_names "Informal Name",
    ce_sample_summary.other_names "Other Names",
    coalesce(ce_sample_summary.time_scale,'') "Time Scale",
    coalesce(ce_sample_summary.minimum_time,'') "Minumum Time",
    coalesce(ce_sample_summary.maximum_time,'') "Maximum Time",
    coalesce(pub_summ.publication_count, 0) "Publication Count",
    coalesce(pub_summ.publication_years, '') "Publication Year",
    coalesce(pub_summ.publication_types,'')  "Publication Type",
    coalesce(pub_summ.authors,'')  "Authors"
--     ,*
from ce_collection_details ced
    left join fossil_sample.mv_ce_sample_summary ce_sample_summary on ce_sample_summary.collection_event_id = ced.resourceinstanceid
    left join ce_location cel on cel.parenttileid = ced.tileid
    left join publication.mv_ce_publication_summary pub_summ on pub_summ.collection_event = ced.resourceinstanceid
order by "Location Descriptor", "Collection Start Year";

create or replace procedure refresh_export_mvs() as
$$
BEGIN
    refresh materialized view fossil_type.mv_fossil_name;
    refresh materialized view fossil_sample.mv_fossil_name;
    refresh materialized view fossil_sample.mv_ce_sample_summary;
    refresh materialized view publication.mv_ce_publication_summary;
END
$$ language plpgsql;

-- select * from fossil_collection_event.collection_event_vw
-- where collection_event_id = '949fab24-8ab3-4433-8325-2beaef949adf'::uuid;

