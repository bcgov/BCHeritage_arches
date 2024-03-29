from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls.resolvers import RegexPattern
from bcrhp.views.api import BordenNumber, MVT
from bcrhp.views.crhp import CRHPXmlExport
from .views.map import BCTileserverProxyView

uuid_regex = settings.UUID_REGEX

print("settings.MEDIA_URL: %s"%settings.MEDIA_URL)
print("settings.MEDIA_ROOT: %s"%settings.MEDIA_ROOT)
class BCRegexPattern(RegexPattern):
    def __init__(self, regexpattern):
        # print("%s -> %s" % (regexpattern.regex.pattern, regexpattern.regex.pattern.replace(r"^", r"^"+settings.BCGOV_PROXY_PREFIX, 1)))
        # print(type(regexpattern))
        # print(type(regexpattern.regex))
        # print(type(regexpattern.regex.pattern))
        super().__init__(regexpattern.regex.pattern.replace(r"^", r"^"+settings.BCGOV_PROXY_PREFIX, 1), regexpattern.name, regexpattern._is_endpoint)

bc_url_resolver = re_path((r'^'), include('arches.urls'))

if settings.BCGOV_PROXY is True:
    for pattern in bc_url_resolver.url_patterns:
        pattern.pattern = BCRegexPattern(pattern.pattern)
        #print(pattern.pattern)
else:
    for pattern in bc_url_resolver.url_patterns:
        print("%s" % pattern.pattern.regex.pattern)


urlpatterns = [
                  re_path(r"^%sbctileserver/(?P<path>.*)$" % settings.BCGOV_PROXY_PREFIX, BCTileserverProxyView.as_view()),
                  re_path(
                      r"^%sborden_number/(?P<resourceinstanceid>%s)$" % (settings.BCGOV_PROXY_PREFIX, uuid_regex),
                      BordenNumber.as_view(),
                      name="borden_number",
                      ),
                  re_path(
                      r"^%scrhp_export/(?P<resourceinstanceid>%s)$" % (settings.BCGOV_PROXY_PREFIX, uuid_regex),
                      CRHPXmlExport.as_view(),
                      name="crhp_export",
                      ),
                  re_path(
                      r"^%smvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % (settings.BCGOV_PROXY_PREFIX, uuid_regex),
                      MVT.as_view(),
                      name="mvt",
                      ),
                  bc_url_resolver,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
