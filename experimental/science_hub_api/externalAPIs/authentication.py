from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKey


class ApiKeyAuthentication(BaseAuthentication):
    HEADER_NAME = 'X-API-KEY'

    def authenticate(self, request):
        api_key = request.headers.get(self.HEADER_NAME)

        if not api_key:
            raise AuthenticationFailed('API-ключ не предоставлен')

        try:
            api_key_instance = ApiKey.objects.get(key=api_key, is_active=True)
        except ApiKey.DoesNotExist:
            raise AuthenticationFailed('Неверный или неактивный API-ключ')

        return (None, api_key_instance)