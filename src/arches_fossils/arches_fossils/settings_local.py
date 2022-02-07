try:
    from .arches_fossils.settings import *
except ImportError:
    pass

###########
# BCGov specific settings. Should these be externalized into separate file?
###########

# Whether we're behind the bcgov proxy server
BCGOV_PROXY = True
# PROXY prefix used - NB - cannot have leading "/", and must have trailing "/"
BCGOV_PROXY_PREFIX = 'int/arches-fossils/'

STATIC_URL = '/'+BCGOV_PROXY_PREFIX+'media/'
ADMIN_MEDIA_PREFIX = STATIC_URL+"admin/"

###########
# End BCGov specific settings.
###########

AUTHENTICATION_BACKENDS = (
    # "arches.app.utils.email_auth_backend.EmailAuthenticationBackend", #Comment out for IDIR
    "oauth2_provider.backends.OAuth2Backend",
    # "django.contrib.auth.backends.ModelBackend",  # this is default # Comment out for IDIR
    # "django.contrib.auth.backends.RemoteUserBackend",
    "arches_fossils.util.auth.backends.BCGovRemoteUserBackend",  # For IDIR authentication
    "guardian.backends.ObjectPermissionBackend",
    "arches.app.utils.permission_backend.PermissionBackend",
)

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    #'arches.app.utils.middleware.TokenMiddleware',
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "arches.app.utils.middleware.ModifyAuthorizationHeader",
    "oauth2_provider.middleware.OAuth2TokenMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "arches_fossils.util.auth.middleware.SiteminderMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "arches.app.utils.middleware.SetAnonymousUser",
]