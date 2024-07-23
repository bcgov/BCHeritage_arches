from django.core.management.base import BaseCommand
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)
class Command(BaseCommand):
    """
    Command to clear the MVT cache

    """

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        cache.clear()
