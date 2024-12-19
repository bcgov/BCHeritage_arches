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