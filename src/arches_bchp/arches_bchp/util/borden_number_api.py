from django.db import connection

from arches.app.models import models
from arches.app.datatypes.datatypes import DataTypeFactory
from django.contrib.gis.geos import Point
from arches.app.utils import geo_utils
import json
from arches_bchp.util.bcrhp_aliases import BCRHPSiteAliases as site_aliases, GraphSlugs as slugs

import urllib
import ssl

# API to get next borden number sequence, check if a borden number already exists and
# reserve a borden number in HRIA
class BordenNumberApi:
    _datatype_factory = None
    _url = "https://openmaps.gov.bc.ca/geo/pub/WHSE_ARCHAEOLOGY.RAAD_BORDENGRID/ows?service=WFS&request=GetFeature&outputFormat=json&version=2.3.0&typeNames=WHSE_ARCHAEOLOGY.RAAD_BORDENGRID&cql_filter=DWITHIN(GEOMETRY,POINT(%s%%20%s),1,meters)"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    geom_node = None
    officially_recognized_node = None

    def __init__(self):
        super().__init__()

    def _initialize_models(self):
        if not self.geom_node or not self.officially_recognized_node:
            self._datatype_factory = DataTypeFactory()
            graph = models.GraphModel.objects.filter(slug=slugs.HERITAGE_SITE).first()
            self.geom_node = models.Node.objects.filter(alias=site_aliases.SITE_GEOMETRY,
                                                        graph=graph).first()
            self.officially_recognized_node = models.Node.objects.filter(alias=site_aliases.OFFICIALLY_RECOGNIZED,
                                                                         graph=graph).first()

    def _get_borden_grid(self, resourceinstanceid):
        tile = models.TileModel.objects.filter(resourceinstance_id=resourceinstanceid,
                                               nodegroup_id=self.geom_node.nodegroup_id).first()
        print("Got tile: %s" % tile)
        datatype = self._datatype_factory.get_instance(self.geom_node.datatype)
        # geometry = datatype.get_display_value(tile, self.node)
        print("Tile data: %s" % tile.data)
        geometry = tile.data[str(self.geom_node.nodeid)]
        

        print('Geometry: %s %s' % (geometry, type(geometry)))
        utils = geo_utils.GeoUtils()
        centroid = utils.get_centroid(geometry)
        print('Centroid: %s %s' % (centroid, type(centroid)))

        pnt = Point(centroid['coordinates'][0], centroid['coordinates'][1], srid=4326)
        desired_srid = 3005
        pnt.transform(desired_srid)
        print("Translated: %s" % pnt.ewkt)
        print("Points: %s, %s" % (pnt.x, pnt.y))

        url = BordenNumberApi._url % (pnt.x, pnt.y)
        print(url)

        borden_grid = None
        with urllib.request.urlopen(url, context=BordenNumberApi.ctx) as response:
            body = json.loads(response.read().decode())
            print("Got body: %s" % body)
            borden_grid = body["features"][0]["properties"]["BORDGRID"]


        # print("Mpt %s" % mpnt)
        return borden_grid

    def get_next_borden_number(self, resourceinstanceid):
        self._initialize_models()
        borden_grid = self._get_borden_grid(resourceinstanceid)
        with connection.cursor() as cursor:
            cursor.execute("SELECT get_next_borden_number(%s)", [borden_grid])
            row = cursor.fetchone()
            print("Got borden number: %s" % row[0])
            return row[0]

    @staticmethod
    def borden_number_exists(borden_number):
        with connection.cursor() as cursor:
            cursor.execute("SET client_min_messages = debug2")
            cursor.execute("select count(*) from imp_hriatst1.tfm_site where bordennumber = %s",[borden_number])
            # cursor.execute("SELECT borden_number_exists(%s)", [borden_number])
            row = cursor.fetchone()
            print("Borden number exists: %s" % row[0])
            return row[0]

    def reserve_borden_number(self, borden_number, resourceinstanceid):
        self._initialize_models()
        is_heritage_site = "Y"
        tile = models.TileModel.objects.filter(resourceinstance_id=resourceinstanceid,
                                               nodegroup_id=self.officially_recognized_node.nodegroup_id).first()

        # print("Got tile: %s" % tile)
        if tile and tile.data:
            is_heritage_site = "Y" if tile.data[str(self.officially_recognized_node.nodeid)] else "N"

        with connection.cursor() as cursor:
            cursor.execute("SELECT reserve_borden_number(%s, %s, %s)", [borden_number, is_heritage_site, resourceinstanceid])
            row = cursor.fetchone()
            print("Reserve borden number: %s" % row[0])
            return row[0]
