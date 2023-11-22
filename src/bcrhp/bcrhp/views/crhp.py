import logging
# from arches.app.models import models
from arches.app.views.api import APIBase
from bcrhp.models import CrhpExportData
from django.http import HttpResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class CRHPXmlExport(APIBase):

    def get_context_data(self, resourceinstanceid):
        context = {}
        try:
            context["data"] = CrhpExportData.objects.get(resourceinstanceid=resourceinstanceid)
            print("site_images type %s" % type(context["data"].site_images))
            print("heritage_themes type %s" % type(context["data"].heritage_themes))
            # context["data"].site_images = json.loads(context["data"].site_images)
            # context["data"].heritage_themes = json.loads(context["data"].heritage_themes)
            # context["data"].functional_state = json.loads(context["data"].functional_state)
            # context["data"].registry_types = json.loads(context["data"].registry_types)
            # context["tiles"] = models.TileModel.objects.filter(resourceinstance_id=resourceinstanceid).all()
            # borden_number_node = models.Node.objects.filter(alias="borden_number").first()
            # borden_number_tile = models.TileModel.objects.filter(nodegroup_id=borden_number_node.nodegroup_id)
            # context["borden_number"] =
        except Exception as e:
            print(e)
        return context

    def get(self, request, resourceinstanceid):
        context = self.get_context_data(resourceinstanceid)
        print(context)
        print(context["data"].resourceinstanceid)

        return render(request, "views/export/crhp_export.xml", context, content_type="application/xml")
