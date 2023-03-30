from arches.app.views.api import MVT as MVTBase
from django.http import HttpResponse, Http404
from django.core.cache import cache
from django.db import connection
from arches.app.utils.permission_backend import (
    get_restricted_instances,
)
from arches.app.models import models
from arches.app.models.system_settings import settings


class MVT(MVTBase):

    def get(self, request, nodeid, zoom, x, y):
        # print("FOSSILS MVT %s" % MVTBase.EARTHCIRCUM)
        if hasattr(request.user, "userprofile") is not True:
            models.UserProfile.objects.create(user=request.user)
        viewable_nodegroups = request.user.userprofile.viewable_nodegroups
        try:
            node = models.Node.objects.get(nodeid=nodeid, nodegroup_id__in=viewable_nodegroups)
        except models.Node.DoesNotExist:
            raise Http404()
        config = node.config
        cache_key = f"mvt_{nodeid}_{zoom}_{x}_{y}"
        tile = cache.get(cache_key)
        if tile is None:
            resource_ids = get_restricted_instances(request.user, allresources=True)
            if len(resource_ids) == 0:
                resource_ids.append("10000000-0000-0000-0000-000000000001")  # This must have a uuid that will never be a resource id.
            resource_ids = tuple(resource_ids)

            if int(zoom) <= int(config["clusterMaxZoom"]):
                print("Using parent")
                return super(MVT, self).get(request, nodeid, zoom, x, y)
            else:
                print("Using app-specific select2")
                with connection.cursor() as cursor:
                    cursor.execute(
                        """SELECT ST_AsMVT(tile, %s, 4096, 'geom', 'id') FROM 
                        (select tileid,
                            id,
                            resourceinstanceid,
                            nodeid,
                            tiledata ->> 'name'    as name,
                            tiledata ->> 'ranking'    as ranking,
                            geom,
                            total
                        from (SELECT tileid,
                            id,
                            get_map_attribute_data(resourceinstanceid, nodeid) AS tiledata,
                            resourceinstanceid,
                            nodeid,
                            ST_AsMVTGeom(
                                geom,
                                TileBBox(%s, %s, %s, 3857)
                            ) AS geom,
                            1 AS total
                        FROM geojson_geometries
                        WHERE nodeid = %s and resourceinstanceid not in %s) AS tile2) as tile;""",
                        [nodeid, zoom, x, y, nodeid, resource_ids],
                    )
                    tile = bytes(cursor.fetchone()[0])
                    # print(str(tile))
                    cache.set(cache_key, tile, settings.TILE_CACHE_TIMEOUT)
        return HttpResponse(tile, content_type="application/x-protobuf")
