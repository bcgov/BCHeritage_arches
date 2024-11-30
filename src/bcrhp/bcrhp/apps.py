from django.apps import AppConfig
from django.conf import settings

from arches.settings_utils import generate_frontend_configuration


class BcrhpConfig(AppConfig):
    name = "bcrhp"
    is_arches_application = True

    def ready(self):
        if settings.APP_NAME.lower() == self.name:
            generate_frontend_configuration()
