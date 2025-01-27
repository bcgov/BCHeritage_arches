create or replace view fossil_sample.geological_age_vw as
select resourceinstanceid                                                                          fossil_sample_uuid,
       __arches_get_node_display_value(tiledata, fossil_sample.geologic_timescale_division_nodeid()) time_scale,
       __bc_format_uncertainty(tiledata, fossil_sample.minimum_time_nodeid(),
                               fossil_sample.minimum_time_uncertain_nodeid())                  minimum_time,
       __bc_format_uncertainty(tiledata, fossil_sample.maximum_time_nodeid(),
                               fossil_sample.maximum_time_uncertain_nodeid())              maximum_time
from tiles
where nodegroupid = fossil_sample.geological_age_nodegroupid();
