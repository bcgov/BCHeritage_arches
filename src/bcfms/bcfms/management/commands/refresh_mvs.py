from django.db import connection
from django.core.management.base import BaseCommand, CommandError
import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    """
    Command to refresh materialized views that support cross-resource model exports

    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cursor = connection.cursor()
        logger.info('Refreshing materialized views')
        try:
            cursor.execute('call refresh_export_mvs()')
            logger.info('Materialized views refreshed successfully')
        except Exception as e:
            logger.error('Unable to refresh materialized views: %s', str(e))
