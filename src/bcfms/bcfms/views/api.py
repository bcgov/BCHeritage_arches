from bcfms.views.mvt_base import MVTConfig, MVT as MVTCommon
from arches.app.views.api import APIBase
from arches.app.utils.response import JSONResponse, JSONErrorResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer
from bcfms.util.business_data_proxy import FossilSampleDataProxy, CollectionEventDataProxy


query_config = {
    '692d8938-9c1d-11ec-a5e5-5254008afee6': ['size_categories'],
    'c66518e2-10c6-11ec-adef-5254008afee6': ['name','ranking'],
    'dd19c7c6-0202-11ed-a511-0050568377a0': ['name','ranking'],
    '2336968c-1035-11ec-a3aa-5254008afee6': ['name','ranking'],
    '4fe7beb2-1f3a-11ed-a99d-5254008afee6': ['name','ranking'],
}

mvt_config = MVTConfig(query_config)
class MVT(MVTCommon):

    def get_mvt_config(self):
        return mvt_config


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
