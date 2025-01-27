create materialized view fossil_sample.fossil_name_mv as
select *
from fossil_sample.fossil_name_vw;
create index fs_fnmv_idx1 on fossil_sample.fossil_name_mv (fossil_sample_uuid);
create index fs_fnmv_idx2 on fossil_sample.fossil_name_mv (scientific_name, other_scientific_name, common_name);
