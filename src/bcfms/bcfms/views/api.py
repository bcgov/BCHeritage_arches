from bcfms.views.mvt_base import MVTConfig, MVT as MVTCommon
from arches.app.views.api import APIBase
from bcfms.functions.bc_fossils_descriptors import BCFossilsDescriptors
from arches.app.models.resource import Resource
from arches.app.utils.response import JSONResponse, JSONErrorResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer, JSONDeserializer


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

        ce_descriptors = BCFossilsDescriptors()
        ce_descriptors.initialize_static_data()

        resource = Resource.objects.filter(
            resourceinstanceid=collection_event_id
        ).first()
        # Expecting an object not a string
        sample_ids = ce_descriptors._get_samples(resource)
        names = ce_descriptors.get_scientific_names_from_samples(sample_ids, formatted=False)
        # print("Scientific Names: %s" % names)
        if len(names) < 1:
            names = ce_descriptors.get_common_names_from_samples(sample_ids, formatted=False)
        names = sorted(list(set(names)))
        return JSONResponse(JSONSerializer().serializeToPython(names))
