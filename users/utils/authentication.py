from django.utils import timezone

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from users.models import Token


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        token = Token.objects.select_related('user').filter(key=key, expires_at__gte=timezone.now()).first()

        if token is None:
            raise AuthenticationFailed({'detail': 'Invalid or expired token.', 'logout': 'true'})

        if not token.user.is_active:
            raise AuthenticationFailed({'detail': 'User inactive or deleted.', 'logout': 'true'})

        if not token.is_active:
            raise AuthenticationFailed({'detail': 'Your token is not active.', 'logout': 'true'})

        return token.user, token