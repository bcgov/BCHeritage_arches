import base64
import logging
import urllib.request
from django.contrib.gis.geos import GEOSGeometry
from django.db import connection
from django.utils.translation import gettext as _
from arches.app.models.system_settings import settings
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from arches.app.search.elasticsearch_dsl_builder import Bool, Nested, Terms, GeoShape
from arches.app.search.components.base import BaseSearchFilter
from arches.app.search.components.map_filter import add_geoshape_query_to_search_query

logger = logging.getLogger(__name__)

details = {
    "searchcomponentid": "",
    "name": "Map Filter",
    "icon": "fa fa-map-marker",
    "modulename": "map_filter.py",
    "classname": "MapFilter",
    "type": "map-filter-type",
    "componentpath": "views/components/search/map-filter",
    "componentname": "map-filter",
    "config": {},
}


class BCMapFilter(BaseSearchFilter):
    def append_dsl(self, search_query_object, **kwargs):
        permitted_nodegroups = kwargs.get("permitted_nodegroups")
        include_provisional = kwargs.get("include_provisional")
        querystring_params = kwargs.get("querystring", "{}")
        try:
            spatial_filter = JSONDeserializer().deserialize(querystring_params)
            if spatial_filter["type"] == "BY_POST":
                querystring_params = self.request.POST.get(details["componentname"], "")
                spatial_filter = JSONDeserializer().deserialize(querystring_params)
        except ValueError:
            querystring_params = self.request.POST.get(details["componentname"], "")
            spatial_filter = JSONDeserializer().deserialize(querystring_params)

        buffered_feature_geoms = []
        spatial_query = Bool()
        if "features" in spatial_filter:
            if len(spatial_filter["features"]) > 0:
                for feature in spatial_filter["features"]:
                    single_feature_search_query = Bool()
                    feature_geom = feature["geometry"]
                    feature_properties = {}
                    if "properties" in feature:
                        feature_properties = feature["properties"]
                    buffered_feature_geom = add_geoshape_query_to_search_query(
                        feature_geom,
                        feature_properties,
                        permitted_nodegroups,
                        include_provisional,
                        single_feature_search_query,
                    )
                    buffered_feature_geoms.append(buffered_feature_geom)

                    # If it's not inverted (filter is set, no must_not) and it's a union, turn it into a should
                    if len(spatial_filter["features"]) > 1 and spatial_filter["operation"] == "union":
                        single_feature_search_query.should(single_feature_search_query.dsl["bool"]["filter"][0])
                        single_feature_search_query.dsl["bool"]["filter"] = []

                    spatial_query.merge(single_feature_search_query)

        search_query_object["query"].add_query(spatial_query)

        if self.componentname not in search_query_object:
            search_query_object[self.componentname] = {}

        try:
            search_query_object[self.componentname]["search_buffer"] = buffered_feature_geoms
        except NameError:
            logger.info(_("Feature geometry is not defined"))
