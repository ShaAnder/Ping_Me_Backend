# webchat/middleware.py

from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    """
    Custom token auth middleware for Django Channels 3.x/4.x
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Import Token model here
        from rest_framework.authtoken.models import Token
        query_string = scope.get('query_string', b'').decode()
        token_key = parse_qs(query_string).get('token')
        user = AnonymousUser()
        if token_key:
            user = await self.get_user(token_key[0])
        scope['user'] = user
        return await self.app(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        from rest_framework.authtoken.models import Token
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()
