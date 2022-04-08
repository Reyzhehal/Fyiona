import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from users.models import CustomUser, UserProfile


class JWTAuthentication(authentication.BaseAuthentication):
    """This Custom class allows to fully overwrite authentication logic and control this process."""

    authentication_header_prefix = "Bearer"

    def authenticate(self, request):
        """Custom authentication function recognize the Bearer token in the request and defines its validity."""
        request.user = None

        # Split Token Filed onto Two Elements: Token {Token Body}
        auth_header = authentication.get_authorization_header(request).split()
        # Change Default Type of Token From "Token" to "Bearer"
        auth_header_prefix = self.authentication_header_prefix

        # There is not field with Token at all
        if not auth_header:
            return None

        # Token missing some information thus, Invalid token header.
        # No credentials provided.
        # Do not attempt to authenticate.
        if len(auth_header) == 1:
            return None

        # If list with Token elements contains more than two objects - Invalid Token.
        # Token must not have any spaces.
        if len(auth_header) > 2:
            return None

        # The Data from Request will be ENCODED into Bytes,
        # so it is better to decode before passing results into JWT decoder.
        prefix = auth_header[0].decode("utf-8")
        token = auth_header[1].decode("utf-8")

        # Prefix of Token has to be "Bearer"
        if prefix != auth_header_prefix:
            return None

        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """Sub function that does the logic to check if recieved token is valid."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
        except jwt.exceptions.DecodeError:
            msg = {
                "success": False,
                "error": "Invalid authentication. Could not decode token.",
            }
            raise exceptions.AuthenticationFailed(msg)
        except jwt.exceptions.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {
                    "success": False,
                    "message": "Session has expired, please login again!",
                }
            )

        try:
            user = CustomUser.objects.get(id=payload["id"])

        except CustomUser.DoesNotExist:
            msg = {
                "success": False,
                "error": "No user matching this token was found...",
            }
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = {
                "success": False,
                "error": f"User {user.username} Has Been Deactivated!",
            }
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
