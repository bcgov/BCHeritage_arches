from io import StringIO
from django.utils.translation import gettext as _
from arches.app.utils.decorators import group_required
from arches.app.views.search import export_results as base_export_results
from arches.app.models.system_settings import settings
import arches.app.utils.zip as zip_utils
from bcrhp.search.search_export import BCRHPSearchResultsExporter


@group_required("Resource Exporter")
def export_results(request):
    # print("In BCGOv specific search results")
    # Merge the GET and POST data. Arches assumes data is in the GET object
    request.GET = request.GET.copy()
    for key, value in request.POST.items():
        # print("%s -> %s" % (key, value))
        request.GET[key] = value

    format = request.GET.get("format", "tilecsv")

    if format == "tilecsv":
        report_link = request.GET.get("reportlink", False)
        exporter = BCRHPSearchResultsExporter(search_request=request)
        export_files, export_info = exporter.export(format, report_link)

        if len(export_files) == 0 and format == "shp":
            message = _(
                "Either no instances were identified for export or no resources have exportable geometry nodes\
                Please confirm that the models of instances you would like to export have geometry nodes and that\
                those nodes are set as exportable"
            )
            dest = StringIO()
            dest.write(message)
            export_files.append({"name": "error.txt", "outputfile": dest})
        return zip_utils.zip_response(export_files, zip_file_name=f"{settings.APP_NAME}_export.zip")

    return base_export_results(request)
