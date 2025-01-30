import os
import logging
from celery import shared_task
from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.utils.translation import gettext as _
from arches.app.models import models
from arches.app.tasks import create_user_task_record, update_user_task_record, log_error
from arches.app.utils.message_contexts import return_message_context
from tempfile import NamedTemporaryFile


@shared_task(bind=True)
def export_search_results(self, userid, request_values, format, report_link):
    from bcfms.search.search_export import (
        BCFMSSearchResultsExporter as SearchResultsExporter,
    )
    from arches.app.models.system_settings import settings

    print("Request Values: %s" % request_values)

    logger = logging.getLogger(__name__)
    settings.update_from_db()

    create_user_task_record(self.request.id, self.name, userid)
    _user = User.objects.get(id=userid)
    try:
        email = request_values["email"]
    except KeyError:
        email = None
    try:
        export_name = request_values["exportName"][0]
    except KeyError:
        export_name = None
    new_request = HttpRequest()
    new_request.method = "GET"
    new_request.user = _user
    for k, v in request_values.items():
        new_request.GET.__setitem__(k, v[0])
    new_request.path = request_values["path"]
    if format == "tilexl":
        exporter = SearchResultsExporter(search_request=new_request)
        export_files, export_info = exporter.export(format, report_link)
        wb = export_files[0]["outputfile"]
        try:
            with NamedTemporaryFile(delete=False) as tmp:
                wb.save(tmp.name)
                tmp.seek(0)
                stream = tmp.read()
                export_files[0]["outputfile"] = tmp
                exportid = exporter.write_export_zipfile(
                    export_files, export_info, export_name
                )
        except OSError:
            logger.error("Temp file could not be created.")
            raise
        os.unlink(tmp.name)
    else:
        exporter = SearchResultsExporter(search_request=new_request)
        files, export_info = exporter.export(format, report_link)
        exportid = exporter.write_export_zipfile(files, export_info, export_name)

    search_history_obj = models.SearchExportHistory.objects.get(pk=exportid)

    expiration_date = datetime.now() + timedelta(
        seconds=settings.CELERY_SEARCH_EXPORT_EXPIRES
    )
    formatted_expiration_date = expiration_date.strftime("%A, %d %B %Y")

    context = return_message_context(
        greeting=_(
            "Hello,\nYour request to download a set of search results is now ready. You have until {} to access this download, after which time it'll be deleted.".format(
                formatted_expiration_date
            )
        ),
        closing_text=_("Thank you"),
        email=email,
        additional_context={
            "link": str(exportid),
            "button_text": _("Download Now"),
            "name": export_name,
            "email_link": get_export_file(exportid),
            "username": _user.first_name or _user.username,
        },
    )

    return {
        "taskid": self.request.id,
        "msg": _(
            "Your search '{}' is ready for download. You have until {} to access this file, after which we'll automatically remove it.".format(
                export_name, formatted_expiration_date
            )
        ),
        "notiftype_name": "Search Export Download Ready",
        "context": context,
    }


def get_export_file(exportid):
    if exportid is not None:
        export = models.SearchExportHistory.objects.get(pk=exportid)
        try:
            url = export.downloadfile.url
            print("URL: %s" % url)
            return url
        except ValueError:
            return None