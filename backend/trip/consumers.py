import json
from channels.generic.websocket import AsyncWebsocketConsumer

import logging

logger = logging.getLogger(__name__)


class TripConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        await self.send(json.dumps({"message": f"Echo message: {data}"}))
