create materialized view mv_bc_statement_of_significance as
select resourceinstanceid,
       defining_elements->'en'->>'value' defining_elements,
       physical_description->'en'->>'value' physical_description,
       document_location->'en'->>'value' document_location,
       __arches_get_concept_label(significance_type) significance_type,
       heritage_value->'en'->>'value' heritage_value
from heritage_site.bc_statement_of_significance sos;
create index sos_ri_idx1 on mv_bc_statement_of_significance(resourceinstanceid);
