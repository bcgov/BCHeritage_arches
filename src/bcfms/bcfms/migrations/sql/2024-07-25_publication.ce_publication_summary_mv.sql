create materialized view publication.ce_publication_summary_mv as
select collection_event,
       array_to_string(array_agg(distinct publication_year order by publication_year), '; ') publication_years,
       array_to_string(array_agg(distinct publication_type order by publication_type),'; ') publication_types,
       array_to_string(array_agg(distinct author_name order by author_name), '; ') authors,
       count(distinct publication_uuid) publication_count
from publication.publication_details_vw
group by collection_event
order by collection_event;
create unique index ce_ps_idx1 on publication.ce_publication_summary_mv(collection_event);
