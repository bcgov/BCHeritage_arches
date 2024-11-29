create materialized view mv_unique_property_address as
select b.* from  heritage_site.instances i,
                 databc.get_first_address(i.resourceinstanceid) b;
create index if not exists mv_ua_idx on mv_unique_property_address(resourceinstanceid);
