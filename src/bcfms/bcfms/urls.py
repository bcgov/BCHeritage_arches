from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.urls.resolvers import RegexPattern
from bcfms.views.api import MVT, CollectionEventFossilNames, ReportNumberGenerator
from bcfms.views.map import BCTileserverProxyView, BCTileserverLocalProxyView
from bcfms.views.search import export_results as bcfms_export_results
import re

uuid_regex = settings.UUID_REGEX


path_prefix_re = re.compile(r'^(\^)(.*)$')
def bc_path_prefix(path):
    if not settings.BCGOV_PROXY_PREFIX:
        return path
    else:
        new_path = path_prefix_re.sub(r"\1%s\2",path)
        return new_path % settings.BCGOV_PROXY_PREFIX

class BCRegexPattern(RegexPattern):
    def __init__(self, regexpattern):
        super().__init__(bc_path_prefix(regexpattern.regex.pattern), regexpattern.name, regexpattern._is_endpoint)

bc_url_resolver = re_path(r'^', include('arches.urls'))

for pattern in bc_url_resolver.url_patterns:
    # print("Before: %s" % pattern.pattern)
    pattern.pattern = BCRegexPattern(pattern.pattern)
    # print("After: %s" % pattern.pattern)

urlpatterns = [
                  re_path(bc_path_prefix(r"^bctileserver/(?P<path>.*)$"), BCTileserverProxyView.as_view()),
                  re_path(bc_path_prefix(r"^bclocaltileserver/(?P<path>.*)$"), BCTileserverLocalProxyView.as_view()),
                  re_path(bc_path_prefix(r"^get_next_report_number/(?P<nodeid>%s)/(?P<typeAbbreviation>%s)$" % (uuid_regex, "[A-Z]{3}")), ReportNumberGenerator.as_view()),
                  re_path(
                      bc_path_prefix(r"^mvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % uuid_regex),
                      MVT.as_view(),
                      name="mvt",
                      ),
                  re_path(bc_path_prefix(r"^collection_event_fossil_names/(?P<collection_event_id>%s|())$" % uuid_regex),
                          CollectionEventFossilNames.as_view(),
                          name="collection_event_fossil_names"),
                  # Override base export results
                  re_path(bc_path_prefix(r"^search/export_results$"), bcfms_export_results, name="export_results"),
                  bc_url_resolver,
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
