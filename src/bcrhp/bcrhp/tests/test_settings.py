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

from bcrhp.settings import *
import arches
import os
import inspect

try:
    from django.utils.translation import gettext_lazy as _
except ImportError:  # unable to import prior to installing requirements.txt in setup.py
    pass

PACKAGE_NAME = "bcrhp"
ROOT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print("Root dir: %s" % ROOT_DIR)
ROOT_DIR = os.path.normpath(os.path.join(ROOT_DIR, "..", "..", "bcrhp"))
print("Root dir: %s" % ROOT_DIR)
ROOT_DIR = os.path.normpath(
    os.path.join("/apps_ux", "projects", "arches-core", "arches")
)
print("Root dir: %s" % ROOT_DIR)
# TEST_ROOT = os.path.normpath(os.path.join(ROOT_DIR, "tests"))
TEST_ROOT = os.path.normpath(
    os.path.join("apps_ux", "projects", "bcrhp", "bcrhp", "tests")
)
# APP_ROOT = os.path.normpath(os.path.join(ROOT_DIR, "bcrhp"))
APP_ROOT = ""
ELASTICSEARCH_HTTP_PORT = 9200

MIN_ARCHES_VERSION = arches.__version__
MAX_ARCHES_VERSION = arches.__version__

# LOAD_V3_DATA_DURING_TESTS = True will engage the most extensive the of the v3
# data migration tests, which could add over a minute to the test process. It's
# recommended that this setting only be set to True in tests/settings_local.py
# and run in specific cases at the discretion of the developer.
LOAD_V3_DATA_DURING_TESTS = False

RESOURCE_GRAPH_LOCATIONS = (os.path.join(TEST_ROOT, "fixtures", "resource_graphs"),)

ONTOLOGY_FIXTURES = os.path.join(TEST_ROOT, "fixtures", "ontologies", "test_ontology")
ONTOLOGY_PATH = os.path.join(TEST_ROOT, "fixtures", "ontologies", "cidoc_crm")

BUSISNESS_DATA_FILES = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
    "user_permission": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "user_permission_cache",
    },
}

ELASTICSEARCH_PREFIX = "test"

TEST_RUNNER = "bcrhp.tests.base_test.ArchesTestRunner"

# could add Chrome, PhantomJS etc... here
LOCAL_BROWSERS = []  # ['Firefox']

# these are set in Travis CI
SAUCE_USERNAME = os.environ.get("SAUCE_USERNAME")
SAUCE_ACCESS_KEY = os.environ.get("SAUCE_ACCESS_KEY")

ENABLE_USER_SIGNUP = True
FORCE_USER_SIGNUP_EMAIL_AUTHENTICATION = True

RUN_LOCAL = True
if SAUCE_USERNAME and SAUCE_ACCESS_KEY:
    RUN_LOCAL = False

# browser/os combinations to use with saucelabs
REMOTE_BROWSERS = [
    # {"platform": "Windows 8.1",
    #  "browserName": "internet explorer",
    #  "version": "11"},
    # {"platform": "Mac OS X 10.9",
    #  "browserName": "chrome",
    #  "version": "53"},
    # {"platform": "Linux",
    #  "browserName": "firefox",
    #  "version": "45"}
]


OVERRIDE_RESOURCE_MODEL_LOCK = True

ENABLE_TWO_FACTOR_AUTHENTICATION = False
FORCE_TWO_FACTOR_AUTHENTICATION = False

DATATYPE_LOCATIONS.append("tests.fixtures.datatypes")
# ELASTICSEARCH_HOSTS = [{"scheme": "http", "host": "localhost", "port": ELASTICSEARCH_HTTP_PORT}]
ELASTICSEARCH_HOSTS = [
    {"scheme": "https", "host": "localhost", "port": ELASTICSEARCH_HTTP_PORT}
]
ELASTICSEARCH_CERT_LOCATION = "/etc/elasticsearch/certs/http_ca.crt"
ELASTICSEARCH_CONNECTION_OPTIONS = {
    "timeout": 30,
    "verify_certs": True,
    "ca_certs": ELASTICSEARCH_CERT_LOCATION,
    "basic_auth": ("arches_test2", "arches_test"),
}

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
    ("en-gb", _("British English")),
    ("es", _("Spanish")),
    ("ar", _("Arabic")),
]

DOCKER = False

try:
    from arches.settings_local import *
except ImportError:
    pass

if DOCKER:
    try:
        from arches.settings_docker import *
    except ImportError:
        pass

ELASTICSEARCH_CONNECTION_OPTIONS["verify_certs"] = True
ELASTICSEARCH_CONNECTION_OPTIONS["ca_certs"] = ELASTICSEARCH_CERT_LOCATION
print(ELASTICSEARCH_CONNECTION_OPTIONS)
print(ROOT_DIR)
print(TEST_ROOT)
