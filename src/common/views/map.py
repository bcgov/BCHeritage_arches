import urllib3
from arches.app.views.map import TileserverProxyView
from django.conf import settings

class BCTileserverLocalProxyView(TileserverProxyView):
    upstream_urls = settings.BC_TILESERVER_URLS
    """
    Subclass of the TileserverProxyView that has multiple upstream servers.
        - the BC_TILESERVER_URLS is a dict with source->upstream URL mapping
        - the request URL must have the source parameter set. If not set it defaults to the parent upstream value
    """
    def __init__(self, *args, **kwargs):
        super(BCTileserverLocalProxyView, self).__init__(*args, **kwargs)


    def get_request_headers(self):
        proxy_source = self.request.GET.get('source', '')
        # print("\tProxy source: %s" % proxy_source)
        if proxy_source in self.upstream_urls:
            self.upstream = self.upstream_urls[proxy_source]

        return super(BCTileserverLocalProxyView, self).get_request_headers()

class BCTileserverProxyView(BCTileserverLocalProxyView):
    """
    Subclass of the TileserverProxyView that has multiple upstream servers.
        - the BC_TILESERVER_URLS is a dict with source->upstream URL mapping
        - the request URL must have the source parameter set. If not set it defaults to the parent upstream value
    """
    def __init__(self, *args, **kwargs):
        super(BCTileserverProxyView, self).__init__(*args, **kwargs)
        # Setup outbound proxy if it is configured
        if hasattr(settings, 'TILESERVER_OUTBOUND_PROXY')  and settings.TILESERVER_OUTBOUND_PROXY:
            # print("Setting outbound proxy to %s" % settings.TILESERVER_OUTBOUND_PROXY)
            self.http = urllib3.ProxyManager(settings.TILESERVER_OUTBOUND_PROXY)
