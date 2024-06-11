from arches.app.functions.base import BaseFunction
from arches.app.models import models
from arches.app.models.resource import Resource

details = {
    "functionid": "60000000-0000-0000-0000-000000001006",
    "name": "Parent Collection Event Refresh",
    "type": "node",
    "description": "Refreshes the primary descriptors for associated collection events",
    "defaultconfig": {"triggering_nodegroups": []},
    "classname": "ParentCollectionEventRefresh",
    "component": "views/components/functions/parent-collection-event-refresh",
}


class ParentCollectionEventRefresh(BaseFunction):
    _ce_sample_node_id = '5e4b75ba-a079-11ec-bc6e-5254008afee6'

    def save(self, tile, request, context):
        pass

    def post_save(self, tile, request, context):
        # Recalculate descriptors and re-index all the collection events that relate to this sample
        resource_refs =  models.ResourceXResource.objects.filter(
            resourceinstanceidto=tile.resourceinstance.resourceinstanceid,
            nodeid=ParentCollectionEventRefresh._ce_sample_node_id
        ).values_list('resourceinstanceidfrom', flat=True)
        collection_events = Resource.objects.filter(resourceinstanceid__in=resource_refs)
        for resource in collection_events:
            resource.save_descriptors()
            resource.index()

    def on_import(self, tile, request):
        pass

    def get(self, tile, request):
        pass

    def delete(self, tile, request):
        pass
