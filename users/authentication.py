import datetime
import pytz
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from users import models

AUTH_FAILED_ERROR = 'Authentication credentials were not provided'
INVALID_TOKEN_ERROR = 'Invalid Token'
TOKEN_EXPIRED_ERROR = 'Token Expired'


class TokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token is None:
            raise exceptions.AuthenticationFailed(AUTH_FAILED_ERROR)
        token = token.split()
        if len(token) != 2 or token[0].lower() != 'token':
            raise exceptions.AuthenticationFailed(AUTH_FAILED_ERROR)
        token = token[1]
        try:
            token = models.Token.objects.get(key=token)
        except models.Token.DoesNotExist:
            raise exceptions.AuthenticationFailed(INVALID_TOKEN_ERROR)

        now = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        if token.expires_at < now or not token.is_active:
            raise exceptions.AuthenticationFailed(TOKEN_EXPIRED_ERROR)
        return token.user, token


class DesignerAuthentication(TokenAuthentication):

    def authenticate(self, request):
        user, token = super().authenticate(request)
        try:
            designer = models.Designer.objects.get(user=user)
        except models.Designer.DoesNotExist:
            raise exceptions.AuthenticationFailed(INVALID_TOKEN_ERROR)
        return user, token
