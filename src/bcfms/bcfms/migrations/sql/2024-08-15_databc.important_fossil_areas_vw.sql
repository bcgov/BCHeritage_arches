create or replace view databc.important_fossil_areas_vw as
select n.resourceinstanceid              area_id,
       n.area_name -> 'en' ->> 'value'   area_name,
       n.description -> 'en' ->> 'value' description,
       b.area_boundary                   area_boundary
from important_fossil_area.area_name n
         join important_fossil_area.area_boundary b on n.resourceinstanceid = b.resourceinstanceid;
