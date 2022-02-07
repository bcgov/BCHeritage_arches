set search_path to 'fossils_data';
select distinct site_id "ResourceID",
                geol_grp "Geological Group",
                geol_form "Geological Formation",
                member "Geological Member",
                sgnfcnc_rd "Geological Significance Ranking Code",
                sgnfcnc_rs "Ranking Detail"
from fiss_ocr_s_obf
order by site_id;
