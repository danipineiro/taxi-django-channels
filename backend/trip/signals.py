import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from trip.models import Trip
from trip.serializers import TripSerializer

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Trip)
def notify_trip_update(sender, instance, created, **kwargs):
    logger.debug("trip tiene cambios!!!!!!")

    async_to_sync(broadcast_estado_trip)(instance)


async def broadcast_estado_trip(instance):
    group_name = "trip"
    channel_layer = get_channel_layer()

    trip_data = TripSerializer(instance).data

    try:
        await channel_layer.group_send(
            group_name, {"type": "send_trip_update", "data": trip_data}
        )
        logger.debug(f"Mensaje enviado al grupo {group_name}: {trip_data}")
    except Exception as e:
        logger.error(f"Error al enviar el mensaje al grupo {group_name}: {str(e)}")
