create or replace view fossil_sample.fossil_name_vw as
select
    resourceinstanceid fossil_sample_uuid,
    __bc_ref_from_tile(tiledata, fossil_sample.scientific_name_nodeid()) scientific_name,
    __arches_get_node_display_value(tiledata, fossil_sample.open_nomanclature_term_nodeid()) name_connector,
    __bc_ref_from_tile(tiledata, fossil_sample.other_scientific_name_nodeid()) other_scientific_name,
    __bc_ref_from_tile(tiledata, fossil_sample.fossil_common_name_nodeid()) common_name,
    __arches_get_node_display_value(tiledata, fossil_sample.fossil_size_category_v_nodeid()) size_category
from tiles where nodegroupid = fossil_sample.bc_fossil_identification_nodegroupid();
