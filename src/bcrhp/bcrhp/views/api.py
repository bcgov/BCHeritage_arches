import logging
from arches.app.views.api import APIBase
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from arches.app.utils.response import JSONResponse
from arches.app.utils.betterJSONSerializer import JSONSerializer
from bcrhp.util.borden_number_api import BordenNumberApi
from bcrhp.views.mvt_base import MVT as MVTCommon, MVTConfig
from bcrhp.util.business_data_proxy import LegislativeActDataProxy

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


class LegislativeAct(APIBase):

    def get(self, request, act_id):
        legislative_act_proxy = LegislativeActDataProxy()
        act = legislative_act_proxy.get_authorities(act_id)
        # print("Scientific Names: %s" % names)
        return JSONResponse(JSONSerializer().serializeToPython(act))


query_config = {
    '1b6235b0-0d0f-11ed-98c2-5254008afee6': ['authorities', 'borden_number'], # Heritage Site
}

mvt_config = MVTConfig(query_config)
class MVT(MVTCommon):

    def get_mvt_config(self):
        return mvt_config
