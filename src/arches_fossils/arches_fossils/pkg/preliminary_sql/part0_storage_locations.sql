set search_path to 'fossils_data';
select concat('STOR',row_number() over ()) "ResourceID" , * from ( select * from (
            select distinct regexp_replace(rpstrs,'=.*$','') "Storage Location Code", 
                            regexp_replace(rpstrs,'^.*=','') "Storage Location Name" 
            from fiss_ocr_s_obf where rpstrs like '%=%' union
            select '', rpstrs from fiss_ocr_s_obf where rpstrs not like '%=%') a
       order by "Storage Location Code", "Storage Location Name") b;
