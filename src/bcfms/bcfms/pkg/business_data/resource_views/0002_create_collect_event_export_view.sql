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

create materialized view fossil_sample.fossil_name_mv as select * from fossil_sample.fossil_name_vw;
create index fs_fnmv_idx1 on fossil_sample.fossil_name_mv(fossil_sample_uuid);
create index fs_fnmv_idx2 on fossil_sample.fossil_name_mv(scientific_name, other_scientific_name, common_name);


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


drop view if exists fossil_type.fossil_name_vw;
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
                 trim(coalesce(parent.name, '') || ' ' || coalesce(child.name,'')) name,
--        parent.name parent_name,
--        child.name child_name,
--        child.parent_name,
                 coalesce(child.name_type, parent.name_type) name_type,
                 coalesce(child.taxonomic_rank, parent.taxonomic_rank) taxonomic_rank
from name_qry child
         left join name_qry parent on child.parent_name::uuid = parent.resourceinstanceid
order by trim(coalesce(parent.name, '') || ' ' || coalesce(child.name,''));
create materialized view fossil_type.fossil_name_mv as select * from fossil_type.fossil_name_vw;
create index ft_fn_mv_idx1 on fossil_type.fossil_name_mv(fossil_name_uuid);

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
-- select * from publication.publication_details_vw;




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
    coalesce(fsri.storage_location_name, '') "Storage Location Name",
    coalesce(fsri.storage_reference, '') "Storage Reference",
    coalesce(array_to_string(scientific_names, '; '), '') "Scientific Names",
    coalesce(array_to_string(common_names, '; '), '') "Common Names",
    coalesce(array_to_string(size_categories, '; '), '') "Size Categories",
    coalesce(fssv.geological_group, '') "Geological Group",
    coalesce(fssv.geological_formation, '') "Geological Formation",
    coalesce(fssv.geological_member, '') "Geological Member",
    coalesce(fssv.informal_name, '') "Informal Name",
    coalesce(fssv.other_name, '') "Other Name",
    coalesce(time_scale,'') "Time Scale",
    coalesce(minimum_time,'') "Minumum Time",
    coalesce(maximum_time,'') "Maximum Time",
    coalesce(ppd.publication_year, '') "Publication Year",
    coalesce(ppd.journal_title,'')  "Journal Title",
    coalesce(ppd.title,'')  "Publication Title",
    coalesce(ppd.publication_type,'') "Publication Type",
    array_to_string(coalesce(ppd.authors, ARRAY[]::text[]), '; ') "Authors"
--     ,*
from ce_collection_details ced
    left join ce_samples_collected cesc on cesc.resourceinstanceid = ced.resourceinstanceid
    left join ce_location cel on cel.parenttileid = ced.tileid
    left join fossil_sample.storage_location_vw fsri on cesc.samples_collected_uuid::uuid = fsri.collected_sample_uuid
    left join fossil_sample.stratigraphy_vw fssv on cesc.samples_collected_uuid = fssv.fossil_sample_uuid
    left join fossil_sample.geological_age_vw fsga on cesc.samples_collected_uuid = fsga.fossil_sample_uuid
    left join (select publication_uuid, collection_event,  journal_title, title, publication_type, publication_year,
                      array_agg(a.author_name) authors
               from publication.publication_details_vw a group by publication_uuid, collection_event,  a.journal_title, a.title, a.publication_type, a.publication_year) ppd on ppd.collection_event = ced.resourceinstanceid
    left join ( select s.fossil_sample_uuid,
                       __bc_unique_array(array_agg(trim(replace(coalesce(s1.name||' ','') || coalesce(s.name_connector||' ','') ||coalesce(s2.name,''), '  ',' ')) order by 1)) scientific_names,
                       __bc_unique_array(array_agg(cn.name)) common_names,
                       __bc_unique_array(array_agg(s.size_category)) size_categories
                from fossil_sample.fossil_name_mv s
                left join fossil_type.fossil_name_mv s1 on s.scientific_name = s1.fossil_name_uuid
                left join fossil_type.fossil_name_mv s2 on s.other_scientific_name = s2.fossil_name_uuid
                left join fossil_type.fossil_name_mv cn on s.common_name = cn.fossil_name_uuid
                                                       group by s.fossil_sample_uuid) c on cesc.samples_collected_uuid::uuid = c.fossil_sample_uuid
order by "Location Descriptor", "Collection Start Year";

create or replace procedure refresh_export_mvs() as
$$
BEGIN
    refresh materialized view fossil_type.fossil_name_mv;
    refresh materialized view fossil_sample.fossil_name_mv;
END
$$ language plpgsql;

-- select * from fossil_collection_event.collection_event_vw
-- where collection_event_id = '949fab24-8ab3-4433-8325-2beaef949adf'::uuid;

