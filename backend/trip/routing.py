from django.urls import path
from trip.consumers import TripConsumer

websocket_urlpatterns = [
    path("ws/trip/", TripConsumer.as_asgi()),
]
