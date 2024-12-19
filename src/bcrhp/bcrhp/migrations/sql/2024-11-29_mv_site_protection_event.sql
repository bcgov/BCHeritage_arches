create materialized view mv_site_protection_event as
select pe.resourceinstanceid,
       bc_right_id,
       designation_or_protection_start_date,
       designation_or_protection_end_date,
       reference_number,
       protection_notes,
       __arches_get_concept_label(la.authority) authority,
       __arches_get_concept_label(la.legal_instrument) legal_instrument,
       la.act_section->'en'->>'value' act_section,
       __arches_get_concept_label(la.recognition_type) recognition_type,
       gn.government_name,
       gn.government_type
--        gn.government_type->'en'->>'value' government_type
from mv_protection_event pe
         join legislative_act.authority la on legislative_act_id = la.resourceinstanceid
         left join mv_government gn on pe.government_id = gn.resourceinstanceid;
create index mv_pe_idx on mv_site_protection_event(resourceinstanceid, bc_right_id);
