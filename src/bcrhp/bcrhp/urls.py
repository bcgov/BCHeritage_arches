from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from bcrhp.views.api import BordenNumber, MVT
from bcrhp.views.crhp import CRHPXmlExport
from .views.map import BCTileserverProxyView

uuid_regex = settings.UUID_REGEX


bc_url_resolver = re_path((r'^'), include('arches.urls'))


urlpatterns = [
                  re_path(r"^%sbctileserver/(?P<path>.*)$", BCTileserverProxyView.as_view()),
                  re_path(
                      r"^%sborden_number/(?P<resourceinstanceid>%s)$" % uuid_regex,
                      BordenNumber.as_view(),
                      name="borden_number",
                      ),
                  re_path(
                      r"^%scrhp_export/(?P<resourceinstanceid>%s)$" % uuid_regex,
                      CRHPXmlExport.as_view(),
                      name="crhp_export",
                      ),
                  re_path(
                      r"^%smvt/(?P<nodeid>%s)/(?P<zoom>[0-9]+|\{z\})/(?P<x>[0-9]+|\{x\})/(?P<y>[0-9]+|\{y\}).pbf$" % uuid_regex,
                      MVT.as_view(),
                      name="mvt",
                      ),
                  bc_url_resolver,
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_LANGUAGE_SWITCH is True:
    urlpatterns = i18n_patterns(*urlpatterns)
