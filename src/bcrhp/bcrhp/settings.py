"""
Django settings for bcrhp project.
"""

import json
import os
from dotenv import load_dotenv
import sys
import ast
import arches
import inspect
import semantic_version
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, is_optional=False):
    msg = "Set the %s environment variable"
    try:
        val = os.environ[var_name]
        return None if val == "None" else val
    except KeyError:
        if is_optional:
            return None
        error_msg = msg % var_name
        raise ImproperlyConfigured(error_msg)


try:
    from arches.settings import *
except ImportError:
    pass

load_dotenv(
    os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], ".env")
)
APP_NAME = "bcrhp"
APP_VERSION = semantic_version.Version(major=1, minor=3, patch=0)
APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# PROXY prefix used - NB - cannot have leading "/", and must have trailing "/"
BCGOV_PROXY_PREFIX = get_env_variable("BCGOV_PROXY_PREFIX")

WEBPACK_LOADER = {
    "DEFAULT": {
        "STATS_FILE": os.path.join(APP_ROOT, "..", "webpack/webpack-stats.json"),
    },
}

DATATYPE_LOCATIONS.append("bcrhp.datatypes")
FUNCTION_LOCATIONS.append("bcrhp.functions")
ETL_MODULE_LOCATIONS.append("bcrhp.etl_modules")
SEARCH_COMPONENT_LOCATIONS.append("bcrhp.search_components")

LOCALE_PATHS.insert(0, os.path.join(APP_ROOT, "locale"))

FILE_TYPE_CHECKING = False
FILE_TYPES = [
    "bmp",
    "gif",
    "jpg",
    "jpeg",
    "pdf",
    "png",
    "psd",
    "rtf",
    "tif",
    "tiff",
    "xlsx",
    "csv",
    "zip",
    "json",
]
FILENAME_GENERATOR = "bcrhp.util.storage_filename_generator.generate_filename"
UPLOADED_FILES_DIR = "uploadedfiles"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("DJANGO_SECRET_KEY")

# options are either "PROD" or "DEV" (installing with Dev mode set gets you extra dependencies)
MODE = get_env_variable("DJANGO_MODE")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(get_env_variable("DJANGO_DEBUG"))

ROOT_URLCONF = "bcrhp.urls"

ELASTICSEARCH_SCHEME = get_env_variable("ES_SCHEME")
ELASTICSEARCH_HTTP_PORT = int(get_env_variable("ES_PORT"))
ELASTICSEARCH_HTTP_HOST = get_env_variable("ES_HOST")
ELASTICSEARCH_HOSTS = [
    {
        "scheme": ELASTICSEARCH_SCHEME,
        "host": ELASTICSEARCH_HTTP_HOST,
        "port": ELASTICSEARCH_HTTP_PORT,
    }
]

# Modify this line as needed for your project to connect to elasticsearch with a password that you generate
# ELASTICSEARCH_CONNECTION_OPTIONS = {"request_timeout": 30, "verify_certs": False, "basic_auth": ("elastic", "E1asticSearchforArche5")}

# If you need to connect to Elasticsearch via an API key instead of username/password, use the syntax below:
# ELASTICSEARCH_CONNECTION_OPTIONS = {"timeout": 30, "verify_certs": False, "api_key": "<ENCODED_API_KEY>"}
# ELASTICSEARCH_CONNECTION_OPTIONS = {"timeout": 30, "verify_certs": False, "api_key": ("<ID>", "<API_KEY>")}

# Your Elasticsearch instance needs to be configured with xpack.security.enabled=true to use API keys - update elasticsearch.yml or .env file and restart.

# Set the ELASTIC_PASSWORD environment variable in either the docker-compose.yml or .env file to the password you set for the elastic user,
# otherwise a random password will be generated.

# API keys can be generated via the Elasticsearch API: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-create-api-key.html
# Or Kibana: https://www.elastic.co/guide/en/kibana/current/api-keys.html

# ELASTICSEARCH_HTTP_PORT = int(get_env_variable("ESPORT")) # this should be in increments of 200, eg: 9400, 9600, 9800
# # see http://elasticsearch-py.readthedocs.org/en/master/api.html#elasticsearch.Elasticsearch
# ELASTICSEARCH_HOSTS = [{"scheme": "https", "host": ELASTICSEARCH_HTTP_HOST, "port": ELASTICSEARCH_HTTP_PORT}]
#
# # How do we handle this across environments?
ELASTICSEARCH_CERT_LOCATION = get_env_variable("ES_CERT_FILE")
ELASTICSEARCH_API_KEY = get_env_variable("ES_API_KEY")
#
# # # If you need to connect to Elasticsearch via an API key instead of username/password, use the syntax below:
if ELASTICSEARCH_CERT_LOCATION and ELASTICSEARCH_API_KEY:
    ELASTICSEARCH_CONNECTION_OPTIONS = {
        "timeout": 30,
        "api_key": ELASTICSEARCH_API_KEY,
        "verify_certs": True,
        "ca_certs": ELASTICSEARCH_CERT_LOCATION,
    }
# a prefix to append to all elasticsearch indexes, note: must be lower case
ELASTICSEARCH_PREFIX = "bcrhp" + get_env_variable("APP_SUFFIX")

ELASTICSEARCH_CUSTOM_INDEXES = []
# [{
#     'module': 'bcrhp.search_indexes.sample_index.SampleIndex',
#     'name': 'my_new_custom_index', <-- follow ES index naming rules
#     'should_update_asynchronously': False  <-- denotes if asynchronously updating the index would affect custom functionality within the project.
# }]

KIBANA_URL = "http://localhost:5601/"
KIBANA_CONFIG_BASEPATH = "kibana"  # must match Kibana config.yml setting (server.basePath) but without the leading slash,
# also make sure to set server.rewriteBasePath: true

LOAD_DEFAULT_ONTOLOGY = False
LOAD_PACKAGE_ONTOLOGIES = True

# This is the namespace to use for export of data (for RDF/XML for example)
# It must point to the url where you host your site
# Make sure to use a trailing slash
PUBLIC_SERVER_ADDRESS = get_env_variable("PUBLIC_SERVER_ADDRESS")

ARCHES_NAMESPACE_FOR_DATA_EXPORT = PUBLIC_SERVER_ADDRESS

DATABASES = {
    "default": {
        "ATOMIC_REQUESTS": False,
        "AUTOCOMMIT": True,
        "CONN_MAX_AGE": 0,
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "HOST": get_env_variable("PGHOST"),
        "NAME": get_env_variable("PGDBNAME"),
        "OPTIONS": {},
        "PASSWORD": get_env_variable("PGPASSWORD"),
        "PORT": "5432",
        "POSTGIS_TEMPLATE": "template_postgis",
        "TEST": {"CHARSET": None, "COLLATION": None, "MIRROR": None, "NAME": None},
        "TIME_ZONE": None,
        "USER": get_env_variable("PGUSERNAME"),
    }
}

HRIA_DATABASE = {
    "USER": get_env_variable("HRIADB_USER"),
    "PASSWORD": get_env_variable("HRIADB_PASSWORD"),
    "HOST": get_env_variable("HRIADB_HOST"),
    "PORT": get_env_variable("HRIADB_PORT"),
    "SERVICE_NAME": get_env_variable("HRIADB_SERVICE_NAME"),
    "APPLICATION_USER": get_env_variable("HRIADB_APPLICATION_USER"),
}

SEARCH_THUMBNAILS = False

INSTALLED_APPS = (
    "webpack_loader",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "django_hosts",
    "arches",
    "arches.app.models",
    "arches.management",
    "guardian",
    "captcha",
    "revproxy",
    "corsheaders",
    "oauth2_provider",
    "django_celery_results",
    # "compressor",
    # "silk",
    "storages",
    "bcrhp",
    "bcgov_arches_common",
)
INSTALLED_APPS += ("arches.app",)

ROOT_HOSTCONF = "bcrhp.hosts"
DEFAULT_HOST = "bcrhp"

AUTHENTICATION_BACKENDS = (
    # "arches.app.utils.email_auth_backend.EmailAuthenticationBackend", #Comment out for IDIR
    "oauth2_provider.backends.OAuth2Backend",
    "bcrhp.util.external_oauth_backend.ExternalOauthAuthenticationBackend",
    # "django.contrib.auth.backends.ModelBackend",  # this is default # Comment out for IDIR
    # "django.contrib.auth.backends.RemoteUserBackend",
    # "bcrhp.util.auth.backends.BCGovRemoteUserBackend",  # For IDIR authentication behind legacy siteminder
    "guardian.backends.ObjectPermissionBackend",
    "arches.app.utils.permission_backend.PermissionBackend",
)

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # "arches.app.utils.middleware.TokenMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "arches.app.utils.middleware.ModifyAuthorizationHeader",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # "bcrhp.util.auth.middleware.SiteminderMiddleware",
    # "bcrhp.util.auth.auth_required_middleware.AuthRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "arches.app.utils.middleware.SetAnonymousUser",
    # "silk.middleware.SilkyMiddleware",
]

MIDDLEWARE.insert(  # this must resolve to first MIDDLEWARE entry
    0, "django_hosts.middleware.HostsRequestMiddleware"
)

MIDDLEWARE.append(  # this must resolve last MIDDLEWARE entry
    "django_hosts.middleware.HostsResponseMiddleware"
)

STATICFILES_DIRS = build_staticfiles_dirs(app_root=APP_ROOT)

TEMPLATES = build_templates_config(
    debug=DEBUG,
    app_root=APP_ROOT,
)

ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS").split()

SYSTEM_SETTINGS_LOCAL_PATH = os.path.join(
    APP_ROOT, "system_settings", "System_Settings.json"
)
WSGI_APPLICATION = "bcrhp.wsgi.application"

# URL that handles the media served from MEDIA_ROOT, used for managing stored files.
# It must end in a slash if set to a non-empty value.
MEDIA_URL = "/files/"

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = os.path.join(APP_ROOT)

# when hosting Arches under a sub path set this value to the sub path eg : "/{sub_path}/"
FORCE_SCRIPT_NAME = get_env_variable("FORCE_SCRIPT_NAME")

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
if BCGOV_PROXY_PREFIX:
    STATIC_URL = "/" + BCGOV_PROXY_PREFIX + "static/"
elif FORCE_SCRIPT_NAME:
    STATIC_URL = FORCE_SCRIPT_NAME + "static/"
else:
    STATIC_URL = "/static/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(APP_ROOT, "staticfiles")

OVERRIDE_RESOURCE_MODEL_LOCK = False

RESOURCE_IMPORT_LOG = os.path.join(APP_ROOT, "logs", "resource_import.log")
DEFAULT_RESOURCE_IMPORT_USER = {"username": "admin", "userid": 1}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",  # DEBUG, INFO, WARNING, ERROR
            "class": "logging.FileHandler",
            "filename": os.path.join(APP_ROOT, "logs", "arches.log"),
            "formatter": "console",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "INFO",
        },
        "arches": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
        "bcrhp": {"handlers": ["file", "console"], "level": "INFO", "propagate": True},
    },
}

# Rate limit for authentication views
# See options (including None or python callables):
# https://django-ratelimit.readthedocs.io/en/stable/rates.html#rates-chapter
RATE_LIMIT = "5/m"

# Sets default max upload size to 15MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 15728640

# Unique session cookie ensures that logins are treated separately for each app
SESSION_COOKIE_NAME = "bcrhp" + get_env_variable("APP_SUFFIX")


# For more info on configuring your cache: https://docs.djangoproject.com/en/2.2/topics/cache/
CACHES = {
    "default": {
        "BACKEND": get_env_variable("CACHE_BACKEND"),
        "LOCATION": get_env_variable("CACHE_BACKEND_LOCATION", is_optional=True),
    },
    "user_permission": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "user_permission_cache",
    },
}

# Hide nodes and cards in a report that have no data
HIDE_EMPTY_NODES_IN_REPORT = True

BYPASS_UNIQUE_CONSTRAINT_TILE_VALIDATION = False
BYPASS_REQUIRED_VALUE_TILE_VALIDATION = False

DATE_IMPORT_EXPORT_FORMAT = (
    "%Y-%m-%d"  # Custom date format for dates imported from and exported to csv
)

# This is used to indicate whether the data in the CSV and SHP exports should be
# ordered as seen in the resource cards or not.
EXPORT_DATA_FIELDS_IN_CARD_ORDER = True

# Identify the usernames and duration (seconds) for which you want to cache the time wheel
CACHE_BY_USER = {"anonymous": 3600 * 24}
TILE_CACHE_TIMEOUT = 600  # seconds
CLUSTER_DISTANCE_MAX = 20000  # meters
GRAPH_MODEL_CACHE_TIMEOUT = None

OAUTH_CLIENT_ID = ""  #'9JCibwrWQ4hwuGn5fu2u1oRZSs9V6gK8Vu8hpRC4'


EXTERNAL_OAUTH_CONFIGURATION = {
    # these groups will be assigned to OAuth authenticated users on their first login
    # "default_user_groups": ["Guest", "Resource Exporter"],
    # claim to be used to assign arches username from
    "uid_claim": "preferred_username",
    # application ID and secret assigned to your arches application
    "app_id": get_env_variable("OAUTH_CLIENT_ID"),
    "app_secret": get_env_variable("OAUTH_CLIENT_SECRET"),
    # provider scopes must at least give Arches access to openid, email and profile
    "scopes": ["openid", "profile", "email"],
    # authorization, token and jwks URIs must be configured for your provider
    "authorization_endpoint": get_env_variable("OAUTH_AUTH_ENDPOINT"),
    "token_endpoint": get_env_variable("OAUTH_TOKEN_ENDPOINT"),
    "jwks_uri": get_env_variable("OAUTH_JWKS_URI"),
    # enforces token validation on authentication, AVOID setting this to False,
    "validate_id_token": True,
}

APP_TITLE = "BC Government | Historic Place Inventory"
COPYRIGHT_TEXT = "All Rights Reserved."
COPYRIGHT_YEAR = "2019"

ENABLE_CAPTCHA = False
# RECAPTCHA_PUBLIC_KEY = ''
# RECAPTCHA_PRIVATE_KEY = ''
# RECAPTCHA_USE_SSL = False
NOCAPTCHA = True
# RECAPTCHA_PROXY = 'http://127.0.0.1:8000'
if DEBUG is True:
    SILENCED_SYSTEM_CHECKS = ["captcha.recaptcha_test_key_error"]


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  #<-- Only need to uncomment this for testing without an actual email server
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST = "apps.smtp.gov.bc.ca"
EMAIL_HOST_USER = "BCHistoricPlacesRegister@gov.bc.ca"
# EMAIL_HOST_PASSWORD = 'xxxxxxx'
# EMAIL_PORT = 587

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_WORKER_NAME = get_env_variable("CELERY_WORKER_NAME")
CELERY_BROKER_URL = get_env_variable(
    "CELERY_BROKER_URL"
)  # RabbitMQ --> "amqp://guest:guest@localhost",  Redis --> "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_RESULT_BACKEND = (
    "django-db"  # Use 'django-cache' if you want to use your cache as your backend
)
CELERY_TASK_SERIALIZER = "json"

CELERY_SEARCH_EXPORT_EXPIRES = 24 * 3600  # seconds
CELERY_SEARCH_EXPORT_CHECK = 3600  # seconds

CELERY_BEAT_SCHEDULE = {
    "delete-expired-search-export": {
        "task": "arches.app.tasks.delete_file",
        "schedule": CELERY_SEARCH_EXPORT_CHECK,
    },
    "notification": {
        "task": "arches.app.tasks.message",
        "schedule": CELERY_SEARCH_EXPORT_CHECK,
        "args": ("Celery Beat is Running",),
    },
}

# Set to True if you want to send celery tasks to the broker without being able to detect celery.
# This might be necessary if the worker pool is regulary fully active, with no idle workers, or if
# you need to run the celery task using solo pool (e.g. on Windows). You may need to provide another
# way of monitoring celery so you can detect the background task not being available.
CELERY_CHECK_ONLY_INSPECT_BROKER = False

CANTALOUPE_DIR = os.path.join(ROOT_DIR, UPLOADED_FILES_DIR)
CANTALOUPE_HTTP_ENDPOINT = "http://localhost:8182/"

ACCESSIBILITY_MODE = True

RENDERERS = [
    {
        "name": "imagereader",
        "title": "Image Reader",
        "description": "Displays most image file types",
        "id": "5e05aa2e-5db0-4922-8938-b4d2b7919733",
        "iconclass": "fa fa-camera",
        "component": "views/components/cards/file-renderers/imagereader",
        "ext": "",
        "type": "image/*",
        "exclude": "tif,tiff,psd",
    },
    {
        "name": "pdfreader",
        "title": "PDF Reader",
        "description": "Displays pdf files",
        "id": "09dec059-1ee8-4fbd-85dd-c0ab0428aa94",
        "iconclass": "fa fa-file",
        "component": "views/components/cards/file-renderers/pdfreader",
        "ext": "pdf",
        "type": "application/pdf",
        "exclude": "tif,tiff,psd",
    },
]

# By setting RESTRICT_MEDIA_ACCESS to True, media file requests outside of Arches will checked against nodegroup permissions.
RESTRICT_MEDIA_ACCESS = True

# By setting RESTRICT_CELERY_EXPORT_FOR_ANONYMOUS_USER to True, if the user is attempting
# to export search results above the SEARCH_EXPORT_IMMEDIATE_DOWNLOAD_THRESHOLD
# value and is not signed in with a user account then the request will not be allowed.
RESTRICT_CELERY_EXPORT_FOR_ANONYMOUS_USER = False

# Dictionary containing any additional context items for customising email templates
EXTRA_EMAIL_CONTEXT = {
    "salutation": _("Hi"),
    "expiration": (
        datetime.now() + timedelta(seconds=CELERY_SEARCH_EXPORT_EXPIRES)
    ).strftime("%A, %d %B %Y"),
}

# see https://docs.djangoproject.com/en/1.9/topics/i18n/translation/#how-django-discovers-language-preference
# to see how LocaleMiddleware tries to determine the user's language preference
# (make sure to check your accept headers as they will override the LANGUAGE_CODE setting!)
# also see get_language_from_request in django.utils.translation.trans_real.py
# to see how the language code is derived in the actual code

####### TO GENERATE .PO FILES DO THE FOLLOWING ########
# run the following commands
# language codes used in the command should be in the form (which is slightly different
# form the form used in the LANGUAGE_CODE and LANGUAGES settings below):
# --local={countrycode}_{REGIONCODE} <-- countrycode is lowercase, regioncode is uppercase, also notice the underscore instead of hyphen
# commands to run (to generate files for "British English, German, and Spanish"):
# django-admin.py makemessages --ignore=env/* --local=de --local=en --local=en_GB --local=es  --extension=htm,py
# django-admin.py compilemessages


# default language of the application
# language code needs to be all lower case with the form:
# {langcode}-{regioncode} eg: en, en-gb ....
# a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

# list of languages to display in the language switcher,
# if left empty or with a single entry then the switch won't be displayed
# language codes need to be all lower case with the form:
# {langcode}-{regioncode} eg: en, en-gb ....
# a list of language codes can be found here http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGES = [
    #   ('de', _('German')),
    ("en", _("English")),
    #   ('en-gb', _('British English')),
    #   ('es', _('Spanish')),
]

# override this to permenantly display/hide the language switcher
SHOW_LANGUAGE_SWITCH = len(LANGUAGES) > 1

try:
    from .package_settings import *
except ImportError:
    try:
        from package_settings import *
    except ImportError as e:
        pass

# This is used for bootstrapping ES and PG security configuration
try:
    from .bcrhp.settings_admin import *
except ImportError:
    try:
        from bcrhp.settings_admin import *
    except ImportError:
        pass

###########
# BCGov specific settings. Should these be externalized into separate file?
###########

WEBPACK_DEVELOPMENT_SERVER_PORT = 9000

ARCHES_NAMESPACE_FOR_DATA_EXPORT = PUBLIC_SERVER_ADDRESS
ADMIN_MEDIA_PREFIX = STATIC_URL + "admin/"

###########
# End BCGov specific settings.
###########


STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AWS_STORAGE_BUCKET_NAME = get_env_variable("S3_BUCKET")
AWS_ACCESS_KEY_ID = get_env_variable("S3_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = get_env_variable("S3_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = "https://nrs.objectstore.gov.bc.ca/"
S3_URL = AWS_S3_ENDPOINT_URL
# We want media to be accessed through the arches app not directly from S3
# MEDIA_URL = AWS_S3_ENDPOINT_URL
AWS_S3_PROXIES = {"https": get_env_variable("S3_PROXIES")}

# CSRF_TRUSTED_ORIGINS = ["https://{{ arches_url_hostname }}"]

# Tileserver proxy configuration
# All tileserver requests go through the BCTileserverProxyView to avoid CORS issues
# There is a local instance of pg_tileserv for overlays that aren't hosted in the BCGW

# This is the default if source isn't set as a parameter in the request
TILESERVER_URL = "https://openmaps.gov.bc.ca/"
BC_TILESERVER_URLS = {
    "maps": "https://maps.gov.bc.ca/",
    "openmaps": TILESERVER_URL,
    "local": "http://localhost:7800/",
}

AUTH_BYPASS_HOSTS = get_env_variable("AUTH_BYPASS_HOSTS")
AUTH_NOACCESS_URL = "https://www2.gov.bc.ca/gov/content/governments/celebrating-british-columbia/historic-places/"

# Need to use an outbound proxy as route to tile servers is blocked by firewall
TILESERVER_OUTBOUND_PROXY = get_env_variable("TILESERVER_OUTBOUND_PROXY")
# END Tileserver proxy configuration

DATE_FORMATS = {
    # Keep index values the same for formats in the python and javascript arrays.
    "Python": [
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S%z",
        "%Y-%m-%d",
        "%Y-%m",
        "%Y",
        "-%Y",
    ],
    "JavaScript": [
        "YYYY-MM-DDTHH:mm:ss.sssZ",
        "YYYY-MM-DDTHH:mm:ssZ",
        "YYYY-MM-DD HH:mm:ssZ",
        "YYYY-MM-DD",
        "YYYY-MM",
        "YYYY",
        "-YYYY",
    ],
    "Elasticsearch": [
        "yyyy-MM-dd'T'HH:mm:ss.SSSZZZZZ",
        "yyyy-MM-dd'T'HH:mm:ss.SSSZ",
        "yyyy-MM-dd'T'HH:mm:ssZZZZZ",
        "yyyy-MM-dd'T'HH:mm:ssZ",
        "yyyy-MM-dd HH:mm:ssZZZZZ",
        "yyyy-MM-dd",
        "yyyy-MM",
        "yyyy",
        "-yyyy",
    ],
}

TIMEWHEEL_DATE_TIERS = {
    "name": "Century",
    "interval": 100,
    "root": True,
    "child": {
        "name": "Half Decade",
        "interval": 5,
        "range": {"min": 1980, "max": 2030},
        # "child": {
        #     "name": "Half decade",
        #     "interval": 5,
        #     "range": {"min": 2010, "max": 2023}
        # }
    },
}
