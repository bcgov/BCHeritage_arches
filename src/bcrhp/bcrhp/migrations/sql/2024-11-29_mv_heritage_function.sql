create materialized view mv_heritage_function as
select resourceinstanceid,
       __arches_get_concept_label(unnest(functional_state)) state_period,
       array_agg(__arches_get_concept_label(functional_category))  functional_states
from heritage_site.heritage_function group by resourceinstanceid,
                                              __arches_get_concept_label(unnest(functional_state));
create index mv_hf_idx on mv_heritage_function(resourceinstanceid);