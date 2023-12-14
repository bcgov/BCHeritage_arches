from django.http.response import HttpResponseRedirect
from django.contrib.auth.middleware import AuthenticationMiddleware
from arches.app.models.system_settings import settings


class AuthRequiredMiddleware(AuthenticationMiddleware):
    # Big-hammer approach - redirect anyone not authenticated to external URL

    def bypass_auth(self, request):
        # print(str(request.META.get('REMOTE_ADDR')))
        # print(str(request.META.get('HTTP_X_FORWARDED_FOR')))
        request_source = request.META.get('REMOTE_ADDR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') is None else request.META.get('HTTP_X_FORWARDED_FOR')
        return request_source in settings.AUTH_BYPASS_HOSTS and request.META.get('HTTP_USER_AGENT').startswith(
            "node-fetch/1.0")

    def process_request(self, request):
        if not request.user.is_authenticated:
            if not self.bypass_auth(request):
                return HttpResponseRedirect(settings.AUTH_NOACCESS_URL)
            else:
                print("Bypassing auth")
        return None
