import re
from typing import Tuple
from django.contrib.auth.models import User, Group
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.dispatch import receiver
from django.urls import reverse
from arches.app.models.system_settings import settings
from arches.app.models.models import ExternalOauthToken
from datetime import datetime, timedelta
import requests
import logging
import jwt
from jwt import PyJWKClient
from requests_oauthlib import OAuth2Session
from arches.app.utils.external_oauth_backend import (
    ExternalOauthAuthenticationBackend as CoreOauthBackend,
)

logger = logging.getLogger(__name__)


class ExternalOauthAuthenticationBackend(CoreOauthBackend):
    # Overrides core class of the same name. Does not allow OAuth users to
    # self-register. Redirects to unauthorized page if user is not already in the
    # system.

    def _clean_username(self, username):
        # DLVR: IDIR = <username>@idir, TEST, PROD: IDIR = idir\\<username>

        return (
            None if username is None else re.sub(r"^idir\\(.*)$", r"\1@idir", username)
        )

    def authenticate(self, request, sso_authentication=False, **kwargs):
        try:
            logger.debug("Authenticating (custom)")
            if not sso_authentication or not request:
                return None

            oauth2_settings = ExternalOauthAuthenticationBackend.get_oauth2_settings()
            validate_id_token = (
                oauth2_settings["validate_id_token"]
                if "validate_id_token" in oauth2_settings
                else True
            )
            uid_claim = oauth2_settings["uid_claim"]
            client_id = oauth2_settings["app_id"]
            app_secret = oauth2_settings["app_secret"]
            redirect_uri = request.build_absolute_uri(
                reverse("external_oauth_callback")
            )
            uid_claim_source = (
                oauth2_settings["uid_claim_source"]
                if "uid_claim_source" in oauth2_settings
                else "id_token"
            )

            oauth = OAuth2Session(
                client_id,
                redirect_uri=redirect_uri,
                state=request.session["oauth_state"],
            )
            try:
                logger.debug(
                    "\n\nEndpoint (custom): %s " % oauth2_settings["token_endpoint"]
                )
                logger.debug(
                    "Auth response (custom): %s" % request.build_absolute_uri()
                )
                token_response = oauth.fetch_token(
                    oauth2_settings["token_endpoint"],
                    authorization_response=request.build_absolute_uri(),
                    client_secret=app_secret,
                    include_client_id=True,
                    proxies={"https": ""},
                )
            except Exception as e:
                logger.error("Error getting id/access tokens", exc_info=True)
                raise e  # raise, otherwise this will mysteriously smother.

            expires_in = token_response["expires_in"]
            id_token = token_response["id_token"]
            access_token = token_response["access_token"]
            refresh_token = (
                token_response["refresh_token"]
                if "refresh_token" in token_response
                else None
            )

            if uid_claim_source == "id_token" and id_token is not None:
                if validate_id_token:
                    alg = jwt.get_unverified_header(id_token)["alg"]
                    jwks_client = PyJWKClient(oauth2_settings["jwks_uri"])
                    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
                    decoded_id_token = jwt.decode(
                        id_token, signing_key.key, audience=client_id, algorithms=[alg]
                    )
                else:
                    decoded_id_token = jwt.decode(
                        id_token, options={"verify_signature": False}
                    )

                username = self._clean_username(
                    decoded_id_token[uid_claim]
                    if decoded_id_token and uid_claim in decoded_id_token
                    else None
                )
            else:  # this can be extended to pull user claims from the oidc user endpoint if desired
                username = None

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                logger.warning("Unregistered user tried to login: %s" % username)
                user = None

            if user is None:
                return None

            token = ExternalOauthAuthenticationBackend.get_token(user)
            if token is not None and token.access_token_expiration > datetime.now():
                logger.debug("Returning user (custom): %s" % user)
                return user

            expiration_date = datetime.now() + timedelta(seconds=int(expires_in))
            ExternalOauthToken.objects.filter(user=user).delete()
            token_record = ExternalOauthToken.objects.create(
                user=user,
                access_token=access_token,
                refresh_token=refresh_token,
                id_token=id_token,
                access_token_expiration=expiration_date,
            )
            token_record.save()
            return user

        except Exception as e:
            logger.error("Error in external oauth backend", exc_info=True)
            raise e

    @receiver(user_logged_in)
    def login(sender, user, request, **kwargs):
        logger.debug("Logging in (custom): %s" % user)
        if (
            user.backend
            == "bcfms.util.auth.external_oauth_backend.ExternalOauthAuthenticationBackend"
        ):
            try:
                token = ExternalOauthAuthenticationBackend.get_token(user)
                request.session.set_expiry(
                    (token.access_token_expiration - datetime.now()).total_seconds()
                )
                logger.debug("Set expiry.")
            except ExternalOauthToken.DoesNotExist:
                pass
