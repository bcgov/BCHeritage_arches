import logging
import os
from arches.app.utils.decorators import group_required
from arches.app.models.system_settings import settings
from django.utils.translation import gettext as _
from io import StringIO
import arches.app.utils.zip as zip_utils
from arches.app.utils.response import JSONResponse, JSONErrorResponse
import arches.app.utils.task_management as task_management
import bcfms.tasks.tasks as tasks
from tempfile import NamedTemporaryFile

logger = logging.getLogger(__name__)


@group_required("Resource Exporter")
def export_results(request):
    # This can't be imported above due to circular reference
    from bcfms.search.search_export import BCFMSSearchResultsExporter
    # Merge the GET and POST data. Arches assumes data is in the GET object
    request.GET = request.GET.copy()
    for key, value in request.POST.items():
        request.GET[key] = value

    total = int(request.GET.get("total", 0))
    format = request.GET.get("format", "tilecsv")
    report_link = request.GET.get("reportlink", False)
    app_name = settings.APP_NAME
    if format == "html":
        download_limit = settings.SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD_HTML_FORMAT
    else:
        download_limit = settings.SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD

    if total > download_limit and format != "geojson":
        if (settings.RESTRICT_CELERY_EXPORT_FOR_ANONYMOUS_USER is True) and (
            request.user.username == "anonymous"
        ):
            message = _(
                "Your search exceeds the {download_limit} instance download limit.  \
                Anonymous users cannot run an export exceeding this limit.  \
                Please sign in with your {app_name} account or refine your search"
            ).format(**locals())
            return JSONResponse({"success": False, "message": message})
        else:
            celery_worker_running = task_management.check_if_celery_available()
            if celery_worker_running is True:
                request_values = dict(request.GET)
                request_values["path"] = request.get_full_path()
                result = tasks.export_search_results.apply_async(
                    (request.user.id, request_values, format, report_link),
                    link=tasks.update_user_task_record.s(),
                    link_error=tasks.log_error.s(),
                )
                message = _(
                    "{total} instances have been submitted for export. \
                    Click the Bell icon to check for a link to download your data"
                ).format(**locals())
                return JSONResponse({"success": True, "message": message})
            else:
                message = _(
                    "Your search exceeds the {download_limit} instance download limit. Please refine your search"
                ).format(**locals())
                return JSONResponse({"success": False, "message": message})

    elif format == "tilexl":
        exporter = BCFMSSearchResultsExporter(search_request=request)
        export_files, export_info = exporter.export(format, report_link)
        wb = export_files[0]["outputfile"]
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                wb.save(tmp.name)
                tmp.seek(0)
                stream = tmp.read()
                export_files[0]["outputfile"] = tmp
                result = zip_utils.zip_response(
                    export_files, zip_file_name=f"{settings.APP_NAME}_export.zip"
                )
        except OSError:
            logger.error("Temp file could not be created.")
            raise
        os.unlink(tmp.name)
        return result
    else:
        exporter = BCFMSSearchResultsExporter(search_request=request)
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
        return zip_utils.zip_response(
            export_files, zip_file_name=f"{settings.APP_NAME}_export.zip"
        )
