create materialized view mv_site_record_admin as
select resourceinstanceid,
       restricted,
       __arches_get_concept_label(bcrhp_submission_status) bcrhp_submission_status,
       __arches_get_concept_label(crhp_submission_status) crhp_submission_status,
       date_submitted_to_crhp,
       federal_id_number
from heritage_site.site_record_admin;
create index mv_sra_idx on mv_site_record_admin(resourceinstanceid);
create index mv_sra_idx2 on mv_site_record_admin(bcrhp_submission_status);