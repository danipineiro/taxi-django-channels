import os
import django

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from trip.routing import websocket_urlpatterns as trip_websockets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()  # ensure Django apps are fully loaded before initializing the ASGI application.

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter(trip_websockets)),
    }
)
