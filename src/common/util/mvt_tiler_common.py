from .mvt_tiler_core import MVTTiler as MVTTiler_Base


class MVTTiler(MVTTiler_Base):

    def __init__(self):
        pass

    query_cache = {}

    @staticmethod
    def get_query_config():
        # Override this method to add business data to the base MVT query
        # Return object structure should be {"<geom node id>": [alias1, alias2,...], }
        return {}

    def get_resource_details_query(self):
        # Uses the get_map_attribute_data(resourceinstanceid, nodeid) database function to get the
        # business data from the appropriate nodes
        return """SELECT ST_AsMVT(tile, %(nodeid)s, 4096, 'geom', 'id') FROM 
                        (select tileid,
                            id,
                            resourceinstanceid,
                            nodeid,
                            featureid,
                            {custom_attributes}
                            geom,
                            total
                        from (SELECT tileid,
                            id,
                            get_map_attribute_data(resourceinstanceid, nodeid) AS tiledata,
                            resourceinstanceid,
                            nodeid,
                            featureid::text AS featureid,
                            ST_AsMVTGeom(
                                geom,
                                TileBBox(%(zoom)s, %(x)s, %(y)s, 3857)
                            ) AS geom,
                            1 AS total
                        FROM geojson_geometries
                        WHERE nodeid = %(nodeid)s 
                        and (st_within(geom, TileBBox(%(zoom)s, %(x)s, %(y)s, 3857))
                               or st_intersects(geom, TileBBox(%(zoom)s, %(x)s, %(y)s, 3857))
                          )
                        and {filter}) AS tile2) as tile;"""

    def format_query(self, query_string, permission_filter, params):
        if "custom_tile_data" in params:
            if params["nodeid"] not in MVTTiler.query_cache:
                if params["custom_tile_data"] is not None:
                    attributes = "\n".join(
                        map(
                            lambda field: "tiledata ->> '{field}' as {field},".format(
                                field=field
                            ),
                            params["custom_tile_data"],
                        )
                    )
                else:
                    attributes = " "
                print("format_query.Attributes: %s" % attributes)
                print("format_query.Query: %s" % query_string)
                MVTTiler.query_cache[params["nodeid"]] = query_string.format(
                    filter=permission_filter, custom_attributes=attributes
                )
            print(
                "Returning query from cache: %s"
                % MVTTiler.query_cache[params["nodeid"]]
            )
            return MVTTiler.query_cache[params["nodeid"]]
        return super().format_query(query_string, permission_filter, params)

    def get_resource_details_query_params(self, base_params):
        return (
            dict(
                base_params,
                **{"custom_tile_data": self.get_query_config()[base_params["nodeid"]]}
            )
            if base_params["nodeid"] in self.get_query_config()
            else dict(base_params, **{"custom_tile_data": None})
        )
