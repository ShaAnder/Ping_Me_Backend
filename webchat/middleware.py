# middleware.py
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return TokenAuthMiddlewareInstance(scope, self)

class TokenAuthMiddlewareInstance:
    def __init__(self, scope, middleware):
        self.scope = dict(scope)
        self.middleware = middleware

    async def __call__(self, receive, send):
        # Import Token model here, inside the coroutine
        from rest_framework.authtoken.models import Token
        query_string = self.scope.get('query_string', b'').decode()
        token_key = parse_qs(query_string).get('token')
        user = AnonymousUser()
        if token_key:
            user = await self.get_user(token_key[0])
        self.scope['user'] = user
        inner = self.middleware.inner(self.scope)
        return await inner(receive, send)

    @database_sync_to_async
    def get_user(self, token_key):
        from rest_framework.authtoken.models import Token
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return AnonymousUser()
