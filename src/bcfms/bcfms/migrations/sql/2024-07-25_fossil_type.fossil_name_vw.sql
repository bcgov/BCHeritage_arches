create view fossil_type.fossil_name_vw as
with name_qry as
         (select resourceinstanceid,
                 tileid,
                 __bc_text_from_tile(tiledata, fossil_Type.name_nodeid())                       name,
                 __bc_ref_from_tile(tiledata, fossil_type.parent_name_nodeid())                 parent_name,
                 __arches_get_node_display_value(tiledata, fossil_type.name_type_nodeid())      name_type,
                 __arches_get_node_display_value(tiledata, fossil_type.taxonomic_rank_nodeid()) taxonomic_rank
          from tiles
          where nodegroupid = fossil_type.name_nodegroupid())
select distinct child.resourceinstanceid                                                              fossil_name_uuid,
--        parent.tileid parent_tile,
--        child.tileid child_tile,
                trim(coalesce(parent.name, '') || ' ' || coalesce(child.name, '') || case
                                                                                         when coalesce(child.taxonomic_rank, parent.taxonomic_rank) = 'Genus'
                                                                                             then ' sp.'
                                                                                         else '' end) name,
--        parent.name parent_name,
--        child.name child_name,
--        child.parent_name,
                coalesce(child.name_type, parent.name_type)                                           name_type,
                coalesce(child.taxonomic_rank, parent.taxonomic_rank)                                 taxonomic_rank
from name_qry child
         left join name_qry parent on child.parent_name::uuid = parent.resourceinstanceid
order by trim(coalesce(parent.name, '') || ' ' || coalesce(child.name, '') ||
              case when coalesce(child.taxonomic_rank, parent.taxonomic_rank) = 'Genus' then ' sp.' else '' end);
