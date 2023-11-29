import logging
# from arches.app.models import models
from arches.app.views.api import APIBase
from bcrhp.models import CrhpExportData
from django.http import HttpResponse
import json
import html2text
import datetime

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

    def set_crhp_authority_value(self, protection_event):
        if protection_event["authority"] == "Provincial":
            protection_event["crhp_authority"] = "Province of British Columbia"
        elif protection_event["legal_instrument"] == "Vancouver Charter" or protection_event["government_name"] == "Vancouver":
            protection_event["crhp_authority"] = "City of Vancouver"
        else:
            protection_event["crhp_authority"] =  "Local Governments (BC)"

    def convert_string_to_date(self, obj, key):
        if obj:
            obj[key] = datetime.datetime.fromisoformat(obj[key])

    def format_event_type(self, se):
        if se["event_type"] == "Construction":
            se["event_type"] = "Construction Date" + (" (circa)" if se["dates_approximate"] else "")
        else:
            se["event_type"] = "Significant Dates"

    def get_context_data(self, resourceinstanceid):
        context = {}
        try:
            context["data"] = CrhpExportData.objects.get(resourceinstanceid=resourceinstanceid)
            print("Site names: %s" % str(context["data"].site_names))
            context["data"].common_names = [ site_name for site_name in context["data"].site_names if site_name["name_type"] == "Common"]
            context["data"].other_names = [ site_name for site_name in context["data"].site_names if site_name["name_type"] != "Common"]
            print("Heritage Categories: %s" % context["data"].heritage_categories)
            if len(context["data"].sos) > 0:
                context["data"].sos.sort(key=lambda x: 0 if x["significance_type"] == "Provincial" else 1)
                context["data"].heritage_value = self.text_converter.handle(context["data"].sos[0]["heritage_value"])
                context["data"].defining_elements = self.text_converter.handle(context["data"].sos[0]["defining_elements"])
                context["data"].pysical_description = self.text_converter.handle(context["data"].sos[0]["physical_description"])
                context["data"].document_location = self.text_converter.handle(context["data"].sos[0]["document_location"])

            print("Protection events %s" % str(context["data"].protection_events))
            for item in context["data"].protection_events:
                print("\tAuthority: %s:%s (%s)" % (item["authority"], item["designation_or_protection_start_date"], type(item["designation_or_protection_start_date"])))

            if len(context["data"].protection_events) > 1:
                print("sorting...")
                context["data"].protection_events.sort(key=lambda x: (1 if x["authority"] == "Provincial" else 0, x["designation_or_protection_start_date"]), reverse=True)

            if len(context["data"].protection_events) > 0:
                self.set_crhp_authority_value(context["data"].protection_events[0])
                self.convert_string_to_date(context["data"].protection_events[0], "designation_or_protection_start_date")

            for item in context["data"].protection_events:
                print("\tAuthority: %s:%s" % (item["authority"], item["designation_or_protection_start_date"]))

            for se in context["data"].significant_events:
                print("Significant event (before): %s" % se)
                self.convert_string_to_date(se, "start_year")
                self.convert_string_to_date(se, "end_year")
                self.format_event_type(se)
                print("Significant event: %s" % se)

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
