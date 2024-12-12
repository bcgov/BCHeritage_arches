"""
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import os

from bcfms.settings import *

PACKAGE_NAME = "bcfms"

PROJECT_TEST_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(PROJECT_TEST_ROOT, "fixtures", "data")

RESOURCE_GRAPH_LOCATIONS = (os.path.join(PROJECT_TEST_ROOT, "..", "bcfms", "pkg", "graphs", "resource_models"),)

# ONTOLOGY_FIXTURES = os.path.join(PROJECT_TEST_ROOT, "fixtures", "ontologies", "test_ontology")
ONTOLOGY_PATH = os.path.join(PROJECT_TEST_ROOT, "fixtures", "ontologies", "cidoc_crm")

BUSINESS_DATA_FILES = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

print ("Host: %s" % get_env_variable("PGHOST"))
DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": get_env_variable("PGHOST"),
        "NAME": "bcfms",
        "OPTIONS": {},
        "PASSWORD": "postgis",
        "PORT": "5432",
        "POSTGIS_TEMPLATE": "template_postgis",
        "TEST": {
            "CHARSET": None,
            "COLLATION": None,
            "MIRROR": None,
            "NAME": None
        },
        "TIME_ZONE": None,
        "USER": "postgres"
    }
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "user_permission": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "user_permission_cache",
    },
}

LOGGING["loggers"]["arches"]["level"] = "ERROR"

ELASTICSEARCH_PREFIX = "test"

#TEST_RUNNER = "arches.test.runner.ArchesTestRunner"
TEST_RUNNER = "tests.base_test.ArchesTestRunner"
SILENCED_SYSTEM_CHECKS.append(
    "arches.W001",  # Cache backend does not support rate-limiting
)

# ELASTICSEARCH_HOSTS = [
#     {"scheme": "http", "host": get_env_variable("ESPORT"), "port": ELASTICSEARCH_HTTP_PORT}
# ]

ELASTICSEARCH_SCHEME = get_env_variable("ES_SCHEME")
ELASTICSEARCH_HTTP_PORT = int(get_env_variable("ES_PORT"))
ELASTICSEARCH_HTTP_HOST = get_env_variable("ES_HOST")
ELASTICSEARCH_HOSTS = [{"scheme": ELASTICSEARCH_SCHEME, "host": ELASTICSEARCH_HTTP_HOST, "port": ELASTICSEARCH_HTTP_PORT}]

ELASTICSEARCH_CERT_LOCATION=get_env_variable("ES_CERT_FILE")
ELASTICSEARCH_API_KEY=get_env_variable("ES_API_KEY")
if ELASTICSEARCH_CERT_LOCATION and ELASTICSEARCH_API_KEY:
    ELASTICSEARCH_CONNECTION_OPTIONS = {"timeout": 30,
                                        "api_key": ELASTICSEARCH_API_KEY,
                                        "verify_certs": True,
                                        "ca_certs": ELASTICSEARCH_CERT_LOCATION
                                        }
# a prefix to append to all elasticsearch indexes, note: must be lower case
ELASTICSEARCH_PREFIX = 'test_bcfms'+get_env_variable("APP_SUFFIX")
