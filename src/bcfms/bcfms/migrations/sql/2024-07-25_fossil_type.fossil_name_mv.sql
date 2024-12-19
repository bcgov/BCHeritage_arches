create materialized view fossil_type.fossil_name_mv as
select *
from fossil_type.fossil_name_vw;
create index ft_fn_mv_idx1 on fossil_type.fossil_name_mv (fossil_name_uuid);
