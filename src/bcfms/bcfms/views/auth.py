from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from arches.app.views.auth import ExternalOauth as CoreExternalOauth
import logging

logger = logging.getLogger(__name__)


class UnauthorizedView(View):
    def get(self, request):
        return render(request, "unauthorized.htm")


class ExternalOauth(CoreExternalOauth):
    # Extends view class of the same name in Arches Core. Allows use of custom external oauth class
    # and redirects to unauthorized page, not login page when not authorized
    @method_decorator(
        csrf_exempt, name="dispatch"
    )  # exempt; returned from other oauth2 authorization server, handled by 'oauth_state' in session
    def callback(request):
        logger.debug("In callback (custom)")
        next_url = (
            request.session["next"] if "next" in request.session else reverse("home")
        )
        logger.debug("Session user (custom): %s" % request.session["user"])
        user = authenticate(
            request, username=request.session["user"], sso_authentication=True
        )
        logger.debug("User (custom): %s" % user)
        return ExternalOauth.log_user_in(request, user, next_url)

    @staticmethod
    def log_user_in(request, user, next_url):
        logger.debug("In ExternalOauth (custom): %s" % user)
        if user is not None:
            login(
                request,
                user,
                backend="bcfms.util.auth.external_oauth_backend.ExternalOauthAuthenticationBackend",
            )
            logger.debug("Next URL: %s" % next_url)
            return redirect(next_url)
        else:
            return redirect("unauthorized")
