import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

from trip.constants import TRIP_GROUP, DRIVERS_GROUP
from user.models import User

logger = logging.getLogger(__name__)


class TripConsumer(AsyncWebsocketConsumer):

    groups = [TRIP_GROUP]

    async def connect(self):
        user = self.scope["user"]
        if user.is_anonymous:
            logger.warning("WebSocket connection rejected: Unauthorized user")
            await self.close()
            return

        if user.type == User.DRIVER:
            await self.channel_layer.group_add(DRIVERS_GROUP, self.channel_name)

        logger.info(f"WebSocket connected: {user}")
        await self.accept()

    async def send_trip_update(self, event):
        trip_data = event["data"]

        logger.debug(
            f"Consumer {self.scope["user"].email}: Sending trip update via WebSocket. Data: {trip_data}"
        )

        await self.send(
            text_data=json.dumps({"type": "trip_update", "content": trip_data})
        )

    async def send_trip_deleted(self, event):
        trip_id = event["data"]["id"]

        logger.debug(
            f"Consumer {self.scope["user"].email}: Sending trip deletion via WebSocket. ID: {trip_id}"
        )

        await self.send(
            text_data=json.dumps({"type": "trip_deleted", "content": {"id": trip_id}})
        )
