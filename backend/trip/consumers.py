import json
from channels.generic.websocket import AsyncWebsocketConsumer

import logging

logger = logging.getLogger(__name__)


class TripConsumer(AsyncWebsocketConsumer):

    groups = ["trip"]

    async def send_trip_update(self, event):
        logger.debug("websocket envia!!!!!")

        trip_data = event["data"]

        await self.send(
            text_data=json.dumps({"type": "trip_update", "content": trip_data})
        )
