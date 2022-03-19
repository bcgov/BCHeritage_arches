from django.http.response import HttpResponseRedirect
from django.contrib.auth.middleware import AuthenticationMiddleware


class AuthRequiredMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                "https://www2.gov.bc.ca/gov/content/industry/natural-resource-use/fossil-management/"
            )
        return None
