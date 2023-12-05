import logging
from arches.app.views.api import APIBase
from django.http import HttpResponse, Http404

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from bcrhp.util.borden_number_api import BordenNumberApi

from arches.app.views.api import MVT as MVTBase
from django.core.cache import cache
from django.db import connection
from arches.app.utils.permission_backend import (
    get_restricted_instances,
)
from arches.app.models import models
from arches.app.models.system_settings import settings

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class BordenNumber(APIBase):
    api = BordenNumberApi()


    # Generate a new borden number in HRIA and return it
    def get(self, request, resourceinstanceid):
        new_borden_number = self.api.get_next_borden_number(resourceinstanceid)
        # print("Got borden grid: %s" % borden_grid)
        return_data = '{"status": "success", "borden_number": "%s"}' % new_borden_number
        return_bytes = return_data.encode("utf-8")
        return HttpResponse(return_bytes , content_type="application/json")

class MVT(MVTBase):

    site_query = """SELECT ST_AsMVT(tile, %(nodeid)s, 4096, 'geom', 'id') FROM 
                        (select tileid,
                            id,
                            resourceinstanceid,
                            nodeid,
                            tiledata ->> 'displayname' as displayname,
                            tiledata ->> 'map_popup' as map_popup,
                            tiledata ->> 'authorities'    as authorities,
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

        if int(zoom) <= int(config["clusterMaxZoom"]):
            print("Using parent")
            return super(MVT, self).get(request, nodeid, zoom, x, y)
        else:
            print("Using app-specific select")
            cache_key = f"mvt_{nodeid}_{zoom}_{x}_{y}"
            tile = cache.get(cache_key)
            if tile is None:
                resource_ids = get_restricted_instances(request.user, allresources=True)
                if len(resource_ids) == 0:
                    resource_ids.append("10000000-0000-0000-0000-000000000001")  # This must have a uuid that will never be a resource id.
                resource_ids = tuple(resource_ids)

                with connection.cursor() as cursor:
                    # print(self.site_query % {"nodeid": nodeid, "zoom": zoom, "x": x, "y": y,
                    #                          "resource_ids": resource_ids})
                    cursor.execute( self.site_query, {"nodeid": nodeid, "zoom": zoom, "x": x, "y":y, "resource_ids": resource_ids } )
                    tile = bytes(cursor.fetchone()[0])
                    # print(str(tile))
                    cache.set(cache_key, tile, settings.TILE_CACHE_TIMEOUT)
        return HttpResponse(tile, content_type="application/x-protobuf")
