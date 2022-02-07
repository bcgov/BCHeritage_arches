set search_path to 'fossils_data';
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
