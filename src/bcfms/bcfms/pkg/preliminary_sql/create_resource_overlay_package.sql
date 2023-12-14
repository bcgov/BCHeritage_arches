drop function if exists get_map_attribute_data;
create or replace function get_map_attribute_data(p_resourceinstanceid uuid, nodeid uuid) returns jsonb as
    $$
declare
    data jsonb;
begin
    if nodeid = '692d8938-9c1d-11ec-a5e5-5254008afee6'::uuid then -- Collection Events
        with collection_events as
            (select jsonb_array_elements(tiledata -> '5e4b75ba-a079-11ec-bc6e-5254008afee6') ->>
                    'resourceId' sampleResourceId
             from tiles
             where resourceinstanceid = p_resourceinstanceid
               and nodegroupid = '5e4b75ba-a079-11ec-bc6e-5254008afee6'),
            samples as (select resourceinstanceid,
                               (tiledata ->> '80f69f30-6f3c-11ed-92e2-5254004d77d3')::uuid size_category_uuid from tiles where nodegroupid = '80f68310-6f3c-11ed-92e2-5254004d77d3')
        select jsonb_build_object('size_categories', jsonb_agg(size_categories), 'both', cardinality(array_agg(size_categories))) from
        (select distinct __arches_get_concept_label(size_category_uuid) size_categories
         into data
        from collection_events ce left join
              samples on samples.resourceinstanceid = ce.sampleResourceId::uuid) a;
    elsif nodeid = 'c66518e2-10c6-11ec-adef-5254008afee6'::uuid then -- Important Fossil Areas
        select jsonb_build_object( 'name', namet.tiledata->'49b837b0-10c7-11ec-81af-5254008afee6'->'en'->>'value',
                                   'ranking', rankt.tiledata -> '69230292-10c7-11ec-8a7a-5254008afee6' -> 'en' ->> 'value')
        into data
        from (select * from tiles where nodegroupid = '49b837b0-10c7-11ec-81af-5254008afee6'::uuid) namet
             left join (select * from tiles where nodegroupid = '69230292-10c7-11ec-8a7a-5254008afee6'::uuid) rankt
              on namet.resourceinstanceid = rankt.resourceinstanceid
        where p_resourceinstanceid = namet.resourceinstanceid::uuid;
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
        from (select * from tiles where nodegroupid = '8d8b71ea-9b47-11ec-b9e6-5254008afee6'::uuid) namet
             left join (select * from tiles where nodegroupid = 'd08d1b72-70d7-11ed-9c1b-5254004d77d3'::uuid) rankt
               on namet.resourceinstanceid = rankt.resourceinstanceid
        where p_resourceinstanceid = namet.resourceinstanceid::uuid;
    elsif nodeid = '4fe7beb2-1f3a-11ed-a99d-5254008afee6'::uuid then -- FRPC Areas
        select jsonb_build_object( 'name', namet.tiledata->'5f809ec0-1f3a-11ed-ab70-5254008afee6'->'en'->>'value',
                                   'ranking', rankt.tiledata -> '5d097acc-1f3a-11ed-ab70-5254008afee6')
        into data
        from (select * from tiles where nodegroupid = '5f809ec0-1f3a-11ed-ab70-5254008afee6'::uuid) namet
             left join (select * from tiles where nodegroupid = '5d097acc-1f3a-11ed-ab70-5254008afee6'::uuid) rankt
              on namet.resourceinstanceid = rankt.resourceinstanceid
        where p_resourceinstanceid = namet.resourceinstanceid::uuid;
    else
            data = '{}'::jsonb;
    end if;
    return data;
end;
$$
    language plpgsql;