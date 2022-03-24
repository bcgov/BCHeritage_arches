from django.http.response import HttpResponseRedirect
from django.contrib.auth.middleware import AuthenticationMiddleware


class AuthRequiredMiddleware(AuthenticationMiddleware):
    # Big-hammer approach - redirect anyone not authenticated to external URL

    def process_request(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("https://www2.gov.bc.ca/gov/content/industry/natural-resource-use/fossil-management/")
        return None