import jwt
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import authentication, exceptions

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            exp = payload['exp']

            if datetime.datetime.fromtimestamp(exp) < datetime.datetime.now():
                return None

            user = User.objects.get(id=user_id)
            return (user, token)
        except (jwt.DecodeError, User.DoesNotExist, IndexError):
            return None

    def authenticate_header(self, request):
        return 'Bearer'