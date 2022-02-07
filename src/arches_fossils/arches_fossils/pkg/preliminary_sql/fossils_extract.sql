--- Fossils data extract
/*
-- Part 1 - Geog Name
select distinct site_id "ResourceID", geogr_name "Geographical Name" from fiss_ocr_s_obf
order by site_id;

-- Part 2 - Location
select distinct site_id "ResourceID",
                loc_detail "Detailed Location",
                loc_desc "Location Description",
                city_town "Nearest Municipality",
                nts_ms_num "NTS Mapsheet Number",
                nts_ms_nam "NTS Mapsheet Name"
from fiss_ocr_s_obf
order by site_id;

-- Part 3 - Spatial Location
select distinct  site_id "ResourceID",
                 'POINT ('|| longitude ||' '||latitude||')' "Spatial Coordinates Geometry"
from fiss_ocr_s_obf
order by site_id;
*/
-- Get list of significant and non-significant fossils and common names. Need to find a way to link the fossil types, alternative
-- scientific names and common names for the BC Fossil Type Model Resource Model
select distinct regexp_replace(unnest(regexp_split_to_array(sig_fossl,';')), '^[ ?]*','') a  from fiss_ocr_s_obf order by a;
select distinct regexp_replace(unnest(regexp_split_to_array(nsig_fossl,';')), '^[ ?]*','') a from fiss_ocr_s_obf order by a;
select distinct regexp_replace(regexp_replace(unnest(regexp_split_to_array(comm_name,';')), '^[ ?]*',''), '[ ?]*$', '') a from fiss_ocr_s_obf order by a;
select distinct sig_fossl, nsig_fossl, comm_name from fiss_ocr_s_obf;

-- Reference Document information extract
select distinct rfrnc_srce, rfrnc_thr, rfrnc_yr, rfrnc_ttle from fiss_ocr_s_obf order by rfrnc_srce, rfrnc_thr, rfrnc_yr, rfrnc_ttle;


-- Part 0 - Storage Locations
select concat('STOR',row_number() over ()) "ResourceID" , * from ( select * from (
            select distinct regexp_replace(rpstrs,'=.*$','') "Storage Location Code",
                            regexp_replace(rpstrs,'^.*=','') "Storage Location Name"
            from fiss_ocr_s_obf where rpstrs like '%=%' union
            select '', rpstrs from fiss_ocr_s_obf where rpstrs not like '%=%') a
       order by "Storage Location Code", "Storage Location Name") b;

-- Part 1 - Location information
select distinct site_id "ResourceID",
                geogr_name "Geographical Name",
                loc_detail "Detailed Location",
                loc_desc "Location Description",
                city_town "Nearest Municipality",
                nts_ms_num "NTS Mapsheet Number",
                nts_ms_nam "NTS Mapsheet Name",
                'POINT ('|| longitude ||' '||latitude||')' "Spatial Coordinates Geometry"
from fiss_ocr_s_obf
order by site_id;

-- Part 2 -
select distinct site_id "ResourceID",
                geol_grp "Geological Group",
                geol_form "Geological Formation",
                member "Geological Member",
                sgnfcnc_rd "Geological Significance Ranking Code",
                sgnfcnc_rs "Ranking Detail"
from fiss_ocr_s_obf
order by site_id;