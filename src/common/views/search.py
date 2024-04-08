from arches.app.utils.decorators import group_required
from arches.app.views.search import export_results as base_export_results


@group_required("Resource Exporter")
def export_results(request):
    # print("In BCGOv specific search results")
    # Merge the GET and POST data. Arches assumes data is in the GET object
    request.GET = request.GET.copy()
    for key, value in request.POST.items():
        # print("%s -> %s" % (key, value))
        request.GET[key] = value

    return base_export_results(request)
