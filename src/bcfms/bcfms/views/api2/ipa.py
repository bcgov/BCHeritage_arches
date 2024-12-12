from http import HTTPStatus

from arches.app.utils.betterJSONSerializer import JSONSerializer
from arches.app.utils.response import JSONErrorResponse, JSONResponse
from arches.app.views.api import APIBase

class IpaValidator(APIBase):
    http_method_names = ["get"]

    def is_name_valid(self, request):
        projectName = request.GET.get("projectName")
