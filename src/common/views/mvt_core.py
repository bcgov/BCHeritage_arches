from arches.app.models.system_settings import settings
from arches.app.views.api import APIBase
from arches.app.models import models
from django.http import Http404, HttpResponse
from django.core.cache import cache
from arches.app.utils.permission_backend import get_restricted_instances
from django.db import connection

class MVT(APIBase):
    # Temporary override of Arches Core MVT to bypass resource restrictions for superusers
    # This is 7.6.x implementation. Should be removed once upgraded to 7.6.x
    EARTHCIRCUM = 40075016.6856
    PIXELSPERTILE = 256

    def get(self, request, nodeid, zoom, x, y):
        if hasattr(request.user, "userprofile") is not True:
            models.UserProfile.objects.create(user=request.user)
        viewable_nodegroups = request.user.userprofile.viewable_nodegroups
        try:
            node = models.Node.objects.get(
                nodeid=nodeid, nodegroup_id__in=viewable_nodegroups
            )
        except models.Node.DoesNotExist:
            raise Http404()
        search_geom_count = 0
        config = node.config
        cache_key = MVT.create_mvt_cache_key(node, zoom, x, y, request.user)
        tile = cache.get(cache_key)
        if tile is None:
            resource_ids = [] if request.user.is_superuser else get_restricted_instances(request.user, allresources=True)
            if len(resource_ids) == 0:
                resource_ids.append(
                    "10000000-0000-0000-0000-000000000001"
                )  # This must have a uuid that will never be a resource id.
            resource_ids = tuple(resource_ids)
            with connection.cursor() as cursor:
                if int(zoom) <= int(config["clusterMaxZoom"]):
                    arc = self.EARTHCIRCUM / ((1 << int(zoom)) * self.PIXELSPERTILE)
                    distance = arc * float(config["clusterDistance"])
                    min_points = int(config["clusterMinPoints"])
                    distance = (
                        settings.CLUSTER_DISTANCE_MAX
                        if distance > settings.CLUSTER_DISTANCE_MAX
                        else distance
                    )

                    count_query = """
                    SELECT count(*) FROM geojson_geometries
                    WHERE
                    ST_Intersects(geom, TileBBox(%s, %s, %s, 3857))
                    AND
                    nodeid = %s and resourceinstanceid not in %s
                    """

                    # get the count of matching geometries
                    cursor.execute(count_query, [zoom, x, y, nodeid, resource_ids])
                    search_geom_count = cursor.fetchone()[0]

                    if search_geom_count >= min_points:
                        cursor.execute(
                            """WITH clusters(tileid, resourceinstanceid, nodeid, geom, cid)
                            AS (
                                SELECT m.*,
                                ST_ClusterDBSCAN(geom, eps := %s, minpoints := %s) over () AS cid
                                FROM (
                                    SELECT tileid,
                                        resourceinstanceid,
                                        nodeid,
                                        geom
                                    FROM geojson_geometries
                                    WHERE
                                    ST_Intersects(geom, TileBBox(%s, %s, %s, 3857))
                                    AND
                                    nodeid = %s and resourceinstanceid not in %s
                                ) m
                            )
                            SELECT ST_AsMVT(
                                tile,
                                %s,
                                4096,
                                'geom',
                                'id'
                            ) FROM (
                                SELECT resourceinstanceid::text,
                                    row_number() over () as id,
                                    1 as total,
                                    ST_AsMVTGeom(
                                        geom,
                                        TileBBox(%s, %s, %s, 3857)
                                    ) AS geom,
                                    '' AS extent
                                FROM clusters
                                WHERE cid is NULL
                                UNION
                                SELECT NULL as resourceinstanceid,
                                    row_number() over () as id,
                                    count(*) as total,
                                    ST_AsMVTGeom(
                                        ST_Centroid(
                                            ST_Collect(geom)
                                        ),
                                        TileBBox(%s, %s, %s, 3857)
                                    ) AS geom,
                                    ST_AsGeoJSON(
                                        ST_Extent(geom)
                                    ) AS extent
                                FROM clusters
                                WHERE cid IS NOT NULL
                                GROUP BY cid
                            ) as tile;""",
                            [
                                distance,
                                min_points,
                                zoom,
                                x,
                                y,
                                nodeid,
                                resource_ids,
                                nodeid,
                                zoom,
                                x,
                                y,
                                zoom,
                                x,
                                y,
                            ],
                        )
                    elif search_geom_count:
                        cursor.execute(
                            """SELECT ST_AsMVT(tile, %s, 4096, 'geom', 'id') FROM (SELECT tileid,
                                id,
                                resourceinstanceid,
                                nodeid,
                                ST_AsMVTGeom(
                                    geom,
                                    TileBBox(%s, %s, %s, 3857)
                                ) AS geom,
                                1 AS total
                            FROM geojson_geometries
                            WHERE nodeid = %s and resourceinstanceid not in %s and (geom && ST_TileEnvelope(%s, %s, %s))) AS tile;""",
                            [nodeid, zoom, x, y, nodeid, resource_ids, zoom, x, y],
                        )
                    else:
                        tile = ""
                else:
                    cursor.execute(
                        """SELECT ST_AsMVT(tile, %s, 4096, 'geom', 'id') FROM (SELECT tileid,
                            id,
                            resourceinstanceid,
                            nodeid,
                            ST_AsMVTGeom(
                                geom,
                                TileBBox(%s, %s, %s, 3857)
                            ) AS geom,
                            1 AS total
                        FROM geojson_geometries
                        WHERE nodeid = %s and resourceinstanceid not in %s and (geom && ST_TileEnvelope(%s, %s, %s))) AS tile;""",
                        [nodeid, zoom, x, y, nodeid, resource_ids, zoom, x, y],
                    )
                tile = bytes(cursor.fetchone()[0]) if tile is None else tile
                cache.set(cache_key, tile, settings.TILE_CACHE_TIMEOUT)
        if not len(tile):
            raise Http404()
        return HttpResponse(tile, content_type="application/x-protobuf")

    def create_mvt_cache_key(node, zoom, x, y, user):
        return f"mvt_{str(node.nodeid)}_{zoom}_{x}_{y}_{user.id}"