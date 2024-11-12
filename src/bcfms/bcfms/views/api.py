from django.http import HttpResponse, Http404
from arches.app.views.api import MVT as MVTBase
from arches.app.views.api import APIBase
from arches.app.utils.response import JSONResponse, JSONErrorResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from bcfms.util.business_data_proxy import FossilSampleDataProxy, CollectionEventDataProxy, IPADataProxy
from arches.app.models import models
from bcfms.util.mvt_tiler import MVTTiler

class MVT(MVTBase):

    def get(self, request, nodeid, zoom, x, y):
        if hasattr(request.user, "userprofile") is not True:
            models.UserProfile.objects.create(user=request.user)
        viewable_nodegroups = request.user.userprofile.viewable_nodegroups
        user = request.user

        tile = MVTTiler().createTile(nodeid, viewable_nodegroups, user, zoom, x, y)
        if not tile or not len(tile):
            raise Http404()
        return HttpResponse(tile, content_type="application/x-protobuf")


class CollectionEventFossilNames(APIBase):

    def get(self, request, collection_event_id):

        collection_event_proxy = CollectionEventDataProxy()
        fossil_sample_proxy = FossilSampleDataProxy()

        sample_ids = collection_event_proxy.get_sample_ids(collection_event_id)

        names = fossil_sample_proxy.get_scientific_names_from_samples(sample_ids)
        # print("Scientific Names: %s" % names)
        if len(names) < 1:
            names = fossil_sample_proxy.get_common_names_from_samples(sample_ids)
        names = sorted(list(set(names)))
        return JSONResponse(JSONSerializer().serializeToPython(names))


class ReportNumberGenerator(APIBase):
    def get(self, request, nodeid, typeAbbreviation):
        report_number = {"status": "success", "report_number": IPADataProxy().get_last_report_id(nodeid, typeAbbreviation)}
        return JSONResponse(JSONSerializer().serializeToPython(report_number))
