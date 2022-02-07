from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls.resolvers import RegexPattern


class BCRegexPattern(RegexPattern):
    def __init__(self, regexpattern):
        super().__init__(regexpattern._regex.replace(r"^", r"^"+settings.BCGOV_PROXY_PREFIX), regexpattern.name, regexpattern._is_endpoint)

bc_url_resolver = url(r'^', include('arches.urls'))

if settings.BCGOV_PROXY is True:
    for pattern in bc_url_resolver.url_patterns:
        pattern.pattern = BCRegexPattern(pattern.pattern)
        #print(pattern.pattern)

urlpatterns = [
    bc_url_resolver,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
