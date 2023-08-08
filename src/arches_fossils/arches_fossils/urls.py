from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls.resolvers import RegexPattern
from arches_fossils.views.api import MVT
from arches_fossils.views.map import BCTileserverProxyView, BCTileserverLocalProxyView

uuid_regex = settings.UUID_REGEX

class BCRegexPattern(RegexPattern):
    def __init__(self, regexpattern):
        super().__init__(regexpattern.regex.pattern.replace(r"^", r"^"+settings.BCGOV_PROXY_PREFIX, 1), regexpattern.name, regexpattern._is_endpoint)

bc_url_resolver = url(r'^', include('arches.urls'))

if settings.BCGOV_PROXY is True:
    for pattern in bc_url_resolver.url_patterns:
        pattern.pattern = BCRegexPattern(pattern.pattern)
        #print(pattern.pattern)

urlpatterns = [
                  url(r"^%sbctileserver/(?P<path>.*)$" % settings.BCGOV_PROXY_PREFIX, BCTileserverProxyView.as_view()),
                  url(r"^%sbclocaltileserver/(?P<path>.*)$" % settings.BCGOV_PROXY_PREFIX, BCTileserverLocalProxyView.as_view()),
                  url(
                      r"^%smvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % (settings.BCGOV_PROXY_PREFIX, uuid_regex),
                      MVT.as_view(),
                      name="mvt",
                      ),
                  bc_url_resolver,
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
