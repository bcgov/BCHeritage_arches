drop function if exists get_map_attribute_data;
create or replace function get_map_attribute_data(p_resourceinstanceid uuid, nodeid uuid) returns jsonb as
    $$
declare
    data jsonb;
begin
    if nodeid = 'c66518e2-10c6-11ec-adef-5254008afee6'::uuid then -- Important Fossil Areas
        select jsonb_build_object( 'name', namet.tiledata->'49b837b0-10c7-11ec-81af-5254008afee6'->'en'->>'value',
                                   'ranking', rankt.tiledata -> '69230292-10c7-11ec-8a7a-5254008afee6' -> 'en' ->> 'value')
        into data
        from (select * from tiles where nodegroupid = '49b837b0-10c7-11ec-81af-5254008afee6'::uuid) namet,
             (select * from tiles where nodegroupid = '69230292-10c7-11ec-8a7a-5254008afee6'::uuid) rankt
        where p_resourceinstanceid = rankt.resourceinstanceid::uuid
          and p_resourceinstanceid = namet.resourceinstanceid::uuid;
    elsif nodeid = 'dd19c7c6-0202-11ed-a511-0050568377a0'::uuid then -- Provincially Protected Sites
        select jsonb_build_object( 'name', namet.tiledata->'dd19fa84-0202-11ed-a511-0050568377a0'->'en'->>'value',
                                   'ranking', '')
        into data
        from (select * from tiles where nodegroupid = 'dd19fa84-0202-11ed-a511-0050568377a0'::uuid) namet
        where p_resourceinstanceid = namet.resourceinstanceid::uuid;
    elsif nodeid = '2336968c-1035-11ec-a3aa-5254008afee6'::uuid then -- BC Fossil Site
        select jsonb_build_object( 'name', namet.tiledata->'8d8b71ea-9b47-11ec-b9e6-5254008afee6'->'en'->>'value',
                                   'ranking', rankt.tiledata -> 'd08d1b72-70d7-11ed-9c1b-5254004d77d3' -> 'en' ->> 'value')
        into data
        from (select * from tiles where nodegroupid = '8d8b71ea-9b47-11ec-b9e6-5254008afee6'::uuid) namet,
             (select * from tiles where nodegroupid = 'd08d1b72-70d7-11ed-9c1b-5254004d77d3'::uuid) rankt
        where p_resourceinstanceid = namet.resourceinstanceid::uuid
        and p_resourceinstanceid = namet.resourceinstanceid::uuid;
    else
            data = '{}'::jsonb;
    end if;
    return data;
end;
$$
    language plpgsql;