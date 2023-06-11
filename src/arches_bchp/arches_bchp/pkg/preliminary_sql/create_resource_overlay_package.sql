drop function if exists get_map_attribute_data;
create or replace function get_map_attribute_data(p_resourceinstanceid uuid, nodeid uuid) returns jsonb as
    $$
declare
    data jsonb;
begin
--     select * from nodes n join  graphs g on g.graphid = n.graphid
--              where alias = 'authority' and g.isresource;
--     select * from values where valueid =
-- select graphs.name->>'en', nodes.*
-- from nodes join graphs on nodes.graphid = graphs.graphid
-- where datatype  = 'geojson-feature-collection'
--     and isresource;
-- select * from nodes where alias ~ 'borden';

--     with auth_value as (select resourceinstanceid,
--                                auth_values.value authority
--                         from tiles t
--                                  left join values auth_values
--                                            on (tiledata ->> '6cc3107c-0d06-11ed-8804-5254008afee6')::uuid =
--                                               auth_values.valueid
--                         where nodegroupid = '6cc30064-0d06-11ed-8804-5254008afee6'::uuid),
--          borden_value as (select resourceinstanceid,
--                                  tiledata -> 'e5ecf044-0d06-11ed-86c8-5254008afee6' -> 'en' ->> 'value' borden_number
--                           from tiles t
--                           where nodegroupid = 'e5ecf044-0d06-11ed-86c8-5254008afee6'::uuid)
--     select distinct b.*, a.authority
--     from borden_value b
--              left join auth_value a on a.resourceinstanceid = b.resourceinstanceid
--     order by b.borden_number;
--
--     select * from nodes where nodes.nodeid = 'e5ecf044-0d06-11ed-86c8-5254008afee6'::uuid;
--
--     select * from nodes where alias = 'authority';

    -- Node ID is the spatial node of the graph
    if nodeid = '1b6235b0-0d0f-11ed-98c2-5254008afee6'::uuid then -- BC Heritage Resource
        with auth_value as (select resourceinstanceid,
                                   array_agg(distinct auth_values.value) authority
                            from tiles t
                                     left join values auth_values
                                               on (tiledata ->> '6cc3107c-0d06-11ed-8804-5254008afee6')::uuid =
                                                  auth_values.valueid
                            where nodegroupid = '6cc30064-0d06-11ed-8804-5254008afee6'::uuid
                            group by resourceinstanceid
        ),
             borden_value as (select resourceinstanceid,
                                     tiledata -> 'e5ecf044-0d06-11ed-86c8-5254008afee6' -> 'en' ->> 'value' borden_number
                              from tiles t
                              where nodegroupid = 'e5ecf044-0d06-11ed-86c8-5254008afee6'::uuid)
        select distinct jsonb_build_object('borden_number', b.borden_number, 'authority', a.authority)
        into data
        from borden_value b
                 left join auth_value a on a.resourceinstanceid = b.resourceinstanceid
        where b.resourceinstanceid = p_resourceinstanceid;
        /*
    elsif nodeid = '1d43b3ba-a31c-11ed-bbb0-5254004d77d3'::uuid then -- Local Government
        select jsonb_build_object( 'name', namet.tiledata->'dd19fa84-0202-11ed-a511-0050568377a0'->'en'->>'value',
                                   'ranking', '')
        into data
        from (select * from tiles where nodegroupid = 'dd19fa84-0202-11ed-a511-0050568377a0'::uuid) namet
        where p_resourceinstanceid = namet.resourceinstanceid::uuid;
         */
    else
            data = '{}'::jsonb;
    end if;
    return data;
end;
$$
    language plpgsql;