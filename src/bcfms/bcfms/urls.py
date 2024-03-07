from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from bcfms.views.api import MVT, CollectionEventFossilNames
from bcfms.views.map import BCTileserverProxyView, BCTileserverLocalProxyView
from bcfms.views.search import export_results as bcfms_export_results

uuid_regex = settings.UUID_REGEX

bc_url_resolver = re_path(r'^', include('arches.urls'))

urlpatterns = [
                  re_path(r"^bctileserver/(?P<path>.*)$", BCTileserverProxyView.as_view()),
                  re_path(r"^bclocaltileserver/(?P<path>.*)$", BCTileserverLocalProxyView.as_view()),
                  re_path(
                      r"^mvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % uuid_regex,
                      MVT.as_view(),
                      name="mvt",
                      ),
                  re_path(r"^collection_event_fossil_names/(?P<collection_event_id>%s|())$" % uuid_regex,
                          CollectionEventFossilNames.as_view(),
                          name="collection_event_fossil_names"),
                  # Override base export results
                  re_path(r"^search/export_results$", bcfms_export_results, name="export_results"),
                  bc_url_resolver,
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
