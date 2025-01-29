from django.db import connection
from django.core.management.base import BaseCommand, CommandError
import logging
from bcrhp.util.buisiness_permission_manager import (
    AdminOnlyPermissionManager,
    HeritageSitePermissionManager,
)
from arches.app.models import models
from arches.app.utils.index_database import index_resources_by_type
from arches.app.models.system_settings import settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Command to refresh materialized views that support the one-row view used by DataBC to create the BCGW layer

    """

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--slugs",
            dest="slugs",
            default=None,
            help="List of graph slugs to reset",
        )
        parser.add_argument(
            "-c",
            "--clear-existing",
            action="store_true",
            dest="clear_existing",
            default=False,
            help="Clear any non-standard permissions",
        )

    def handle(self, *args, **options):
        slugs = (
            [slug.strip() for slug in options["slugs"].split(",")]
            if options["slugs"]
            else None
        )
        processed_slugs = AdminOnlyPermissionManager().reset_all_permissions(
            graph_slugs=slugs, clear_all_permissions=options["clear_existing"]
        )
        processed_slugs += HeritageSitePermissionManager().reset_all_permissions(
            graph_slugs=slugs, clear_all_permissions=options["clear_existing"]
        )

        print("Processed graphs: %s" % processed_slugs)
        resource_types_uuid = (
            models.GraphModel.objects.filter(slug__in=processed_slugs)
            .exclude(publication=None)
            .values_list("graphid", flat=True)
        )

        index_resources_by_type(
            resource_types_uuid,
            clear_index=True,
            batch_size=settings.BULK_IMPORT_BATCH_SIZE,
            quiet=False,
            recalculate_descriptors=False,
        )
