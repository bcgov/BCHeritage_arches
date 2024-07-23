from django.http import HttpResponse, Http404

from .mvt_core import MVT as MVTBase
from django.core.cache import cache
from django.db import connection
from arches.app.utils.permission_backend import (
    get_restricted_instances,
)
from arches.app.models import models
from arches.app.models.system_settings import settings

class MVTConfig:

    # object with nodeid: ['field1','field2','field3'...] lookup
    __query_config = {}

    def __init__(self, config):
        self.__query_config = config

    def get_config(self, nodeid):
        return self.__query_config[nodeid]

    def has_config(self, nodeid):
        return nodeid in self.__query_config


class MVTQueryGenerator:

    query_cache = {}
    base_query = """SELECT ST_AsMVT(tile, %(nodeid)s, 4096, 'geom', 'id') FROM 
                        (select tileid,
                            id,
                            resourceinstanceid,
                            nodeid,
                            {}
                            geom,
                            total
                        from (SELECT tileid,
                            id,
                            get_map_attribute_data(resourceinstanceid, nodeid) AS tiledata,
                            resourceinstanceid,
                            nodeid,
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
                        and resourceinstanceid not in %(resource_ids)s) AS tile2) as tile;"""

    @staticmethod
    def format_query(nodeid, config):
        if nodeid not in MVTQueryGenerator.query_cache:
            print("Generating query")
            attributes = "\n".join(map(lambda field: "tiledata ->> '%s' as %s," % (field, field), config))
            MVTQueryGenerator.query_cache[nodeid] = MVTQueryGenerator.base_query.format(attributes)
        print("Returning query from cache")
        return MVTQueryGenerator.query_cache[nodeid]


## This can be extended to provide resource overlays with additional attribute data
class MVT(MVTBase):

    def get_mvt_config(self):
        return MVTConfig({})

    def get(self, request, nodeid, zoom, x, y):
        # print("BCRHP MVT %s" % MVTBase.EARTHCIRCUM)
        if hasattr(request.user, "userprofile") is not True:
            models.UserProfile.objects.create(user=request.user)
        viewable_nodegroups = request.user.userprofile.viewable_nodegroups
        try:
            node = models.Node.objects.get(nodeid=nodeid, nodegroup_id__in=viewable_nodegroups)
        except models.Node.DoesNotExist:
            raise Http404()
        config = node.config

        if int(zoom) <= int(config["clusterMaxZoom"]) or not self.get_mvt_config().has_config(nodeid):
            # print("Using parent")
            return super(MVT, self).get(request, nodeid, zoom, x, y)
        else:
            # print("Using app-specific select with generated query")
            cache_key = MVT.create_mvt_cache_key(node, zoom, x, y, request.user)
            tile = cache.get(cache_key)
            if tile is None:
                resource_ids = [] if request.user.is_superuser else get_restricted_instances(request.user, allresources=True)
                if len(resource_ids) == 0:
                    resource_ids.append("10000000-0000-0000-0000-000000000001")  # This must have a uuid that will never be a resource id.
                resource_ids = tuple(resource_ids)

                with connection.cursor() as cursor:
                    # print(self.site_query % {"nodeid": nodeid, "zoom": zoom, "x": x, "y": y,
                    #                          "resource_ids": resource_ids})
                    cursor.execute(
                        MVTQueryGenerator.format_query(nodeid, self.get_mvt_config().get_config(nodeid)),
                        # self.site_query,
                        {"nodeid": nodeid, "zoom": zoom, "x": x, "y":y, "resource_ids": resource_ids } )
                    tile = bytes(cursor.fetchone()[0])
                    # print(str(tile))
                    cache.set(cache_key, tile, settings.TILE_CACHE_TIMEOUT)
        return HttpResponse(tile, content_type="application/x-protobuf")
