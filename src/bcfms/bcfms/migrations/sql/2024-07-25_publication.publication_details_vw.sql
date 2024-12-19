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
