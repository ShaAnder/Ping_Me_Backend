from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken

User = get_user_model()

class JWTAuthMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope.get('query_string', b'').decode()
        token_list = parse_qs(query_string).get('token')
        user = AnonymousUser()
        if token_list:
            user = await self.get_user(token_list[0])
        scope['user'] = user
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, raw_token):
        try:
            validated_token = UntypedToken(raw_token)
            jwt_auth = JWTAuthentication()
            user = jwt_auth.get_user(validated_token)
            return user
        except (InvalidToken, TokenError, User.DoesNotExist):
            return AnonymousUser()
