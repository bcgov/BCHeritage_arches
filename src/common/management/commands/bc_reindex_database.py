from arches.app.models import models
from django.core.management.base import BaseCommand, CommandError
from arches.app.utils.index_database import index_resources_by_type, index_concepts
from arches.app.models.system_settings import settings
from ..data.index_order import get_index_order


class Command(BaseCommand):
    """
    Custom ES reindex command to take resource dependency into account

    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.reindex_database()


    def reindex_database(self, clear_index=True, batch_size=settings.BULK_IMPORT_BATCH_SIZE, quiet=False):
        resource_types_uuid = []
        index_concepts(clear_index=clear_index, batch_size=batch_size)
        resource_types = (
            models.GraphModel.objects.filter(isresource=True)
            .exclude(graphid=settings.SYSTEM_SETTINGS_RESOURCE_MODEL_ID)
            .exclude(publication=None)
            .values_list("slug", "graphid")
        )
        # print("Before: %s" % str(resource_types))
        index_order = get_index_order()
        # print("Index order: %s" % str(index_order))
        resource_types = sorted(resource_types, key=lambda val: 100 if val[0] not in index_order else index_order.index(val[0]))
        # for val in resource_types:
        #     print("%s: %s" % (val[0], 100 if val[0] not in index_order else index_order.index(val[0])))
        for rt in resource_types:
            resource_types_uuid.append(rt[1])
        # print("After: %s" % str(resource_types_uuid))

        index_resources_by_type(
            resource_types_uuid,
            clear_index=clear_index,
            batch_size=batch_size,
            quiet=quiet,
            recalculate_descriptors=True,
        )

        # index_custom_indexes(clear_index=clear_index, batch_size=batch_size, quiet=quiet)