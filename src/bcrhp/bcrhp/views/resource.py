from arches.app.views.resource import ResourceReportView as ResourceReportViewCore
from arches.app.utils.decorators import group_required
from django.utils.decorators import method_decorator


@method_decorator(group_required("Resource Editor"), name="dispatch")
class ResourceReportView(ResourceReportViewCore):

    def get(self, request, resourceid=None):
        return super().get(request, resourceid)
