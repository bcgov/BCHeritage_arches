import logging
# from arches.app.models import models
from arches.app.views.api import APIBase
from bcrhp.models import CrhpExportData
from django.http import HttpResponse
import json
import html2text

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name="dispatch")
class CRHPXmlExport(APIBase):
    def __init__(self):
        self.text_converter = html2text.HTML2Text()
        self.text_converter.ul_item_mark = '-'
        self.text_converter.wrap_list_items = False
        self.text_converter.body_width = 10000

    def get_context_data(self, resourceinstanceid):
        context = {}
        try:
            context["data"] = CrhpExportData.objects.get(resourceinstanceid=resourceinstanceid)
            print("Site names: %s" % str(context["data"].site_names))
            context["data"].common_names = [ site_name for site_name in context["data"].site_names if site_name["name_type"] == "Common"]
            context["data"].other_names = [ site_name for site_name in context["data"].site_names if site_name["name_type"] != "Common"]
            context["data"].heritage_value = self.text_converter.handle(context["data"].heritage_value)
            context["data"].defining_elements = self.text_converter.handle(context["data"].defining_elements)
            print("site_images type %s" % type(context["data"].site_images))
            print("heritage_themes type %s" % type(context["data"].heritage_themes))
        except Exception as e:
            print(e)
        return context

    def get(self, request, resourceinstanceid):
        context = self.get_context_data(resourceinstanceid)
        print(context)
        print(context["data"].resourceinstanceid)

        return render(request, "views/export/crhp_export.xml", context, content_type="application/xml")
