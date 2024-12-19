from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("bcrhp", "1081_recreate_materialized_views")]

    add_missing_featureids = """
        DO $$
        declare
            json_row record;
            features jsonb;
            feature jsonb;
        BEGIN
            for json_row in
                SELECT t.tileid,
                       t.resourceinstanceid,
                       n.nodeid,
                       t.tiledata,
                       t.tiledata::jsonb -> n.nodeid::text -> 'features' as features,
                       jsonb_array_elements(
                               t.tiledata -> n.nodeid::text -> 'features'
                           ) -> 'geometry'
                                                                        AS geom
                FROM tiles t
                         LEFT JOIN nodes n ON t.nodegroupid = n.nodegroupid
        --         where t.tileid = coalesce(tile_id, t.tileid)
                GROUP BY t.tileid, t.resourceinstanceid, n.nodeid
                HAVING n.datatype = 'geojson-feature-collection'::text
        --         limit 10
                loop
                    features := '[]'::jsonb;
                    for feature in select jsonb_array_elements(json_row.features) loop
                        if feature->>'id' is null then
        --                     raise notice 'Feature before: %', feature::text;
                            feature := jsonb_set(feature, '{id}'::text[], ('"'||uuid_generate_v4()::text||'"')::jsonb);
        --                     raise notice 'Feature: %', feature::text;
                        else
                            raise notice 'Skipping tile.';
                        end if;
                        features := features || jsonb_build_array(feature);
                    end loop;
        --             raise notice 'Features: %', features::text;
                    update tiles set tiledata = jsonb_set(tiledata, ('{'||json_row.nodeid||',"features"}')::text[], features) where tileid = json_row.tileid;
                end loop;
            end
        $$ language plpgsql;
        """

    operations = [
        migrations.RunSQL(add_missing_featureids, migrations.RunSQL.noop),
        migrations.RunSQL(
            "select refresh_geojson_geometries()", migrations.RunSQL.noop
        ),
    ]
