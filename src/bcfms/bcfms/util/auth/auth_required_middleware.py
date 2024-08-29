from django.http.response import HttpResponseRedirect
from django.contrib.auth.middleware import AuthenticationMiddleware
from arches.app.models.system_settings import settings
import re


class AuthRequiredMiddleware(AuthenticationMiddleware):
    # Redirect any unauthenticated users to home page
    _valid_urls = []

    def _clean_path(self, path):
        return re.sub(r"^/*", "", re.sub("/*$", "", path))

    def _get_base_url(self):
        return self._clean_path(
            settings.FORCE_SCRIPT_NAME
            if settings.FORCE_SCRIPT_NAME
            else settings.BCGOV_PROXY_PREFIX
        )

    def _get_public_urls(self):
        if len(AuthRequiredMiddleware._valid_urls) == 0:
            base_url = self._get_base_url()
            for suffix in [
                "",
                "/auth",
                "/auth/eoauth_start",
                "/auth/eoauth_cb",
                "/unauthorized",
            ]:
                AuthRequiredMiddleware._valid_urls.append("%s%s" % (base_url, suffix))
        return AuthRequiredMiddleware._valid_urls

    def _is_public_path(self, path):
        cleaned_path = self._clean_path(path)
        return cleaned_path in self._get_public_urls()

    def bypass_auth(self, request):
        request_source = (
            request.META.get("REMOTE_ADDR")
            if request.META.get("HTTP_X_FORWARDED_FOR") is None
            else request.META.get("HTTP_X_FORWARDED_FOR")
        )
        # return True
        return (
            self._is_public_path(request.path)
            or request_source in settings.AUTH_BYPASS_HOSTS
            and request.META.get("HTTP_USER_AGENT").startswith("node-fetch/1.0")
        )

    def process_request(self, request):
        if not request.user.is_authenticated:
            if not self.bypass_auth(request):
                return HttpResponseRedirect("/%s/" % self._get_base_url())
            else:
                print("Bypassing auth")
        return None
