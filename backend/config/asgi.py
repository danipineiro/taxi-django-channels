import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from trip.routing import websocket_urlpatterns as trip_websockets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = ProtocolTypeRouter(
    {
        "websocket": AuthMiddlewareStack(URLRouter([trip_websockets])),
    }
)
