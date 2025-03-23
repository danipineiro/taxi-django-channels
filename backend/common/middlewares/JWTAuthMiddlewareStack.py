import django

django.setup()

import jwt
import logging
from urllib.parse import parse_qs
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from jwt import DecodeError, ExpiredSignatureError, InvalidSignatureError
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections

User = get_user_model()

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseMiddleware):
    """Middleware to authenticate user for WebSocket connections using JWT."""

    async def __call__(self, scope, receive, send):
        """Authenticate the user based on JWT in the query string."""
        close_old_connections()

        token = parse_qs(scope["query_string"].decode("utf8")).get("token", [None])[0]

        if token:
            token = token.strip('"')
            try:
                data = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                scope["user"] = await self.get_user(data["user_id"])
            except (
                InvalidSignatureError,
                ExpiredSignatureError,
                DecodeError,
                KeyError,
            ) as e:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return AnonymousUser()


def JWTAuthMiddlewareStack(app):
    """Wraps the Django Channels authentication stack with JWTAuthMiddleware."""
    return JWTAuthMiddleware(AuthMiddlewareStack(app))
