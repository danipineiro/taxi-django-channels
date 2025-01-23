import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from trip.constants import TRIP_GROUP
from trip.models import Trip
from trip.serializers import TripSerializer

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Trip)
def notify_trip_update(sender, instance, created, **kwargs):
    """
    Signal triggered when a Trip instance is saved.
    Notifies the trip group about the updated instance.
    """
    action = "created" if created else "updated"
    logger.info(f"Trip {instance.id} has been {action}. Broadcasting changes.")

    async_to_sync(broadcast_trip_state)(instance)


async def broadcast_trip_state(instance):
    """
    Broadcasts trip update to the specified group using Django Channels.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.warning("Channel layer not configured. Skipping broadcast.")
        return

    trip_data = TripSerializer(instance).data

    try:
        await channel_layer.group_send(
            TRIP_GROUP, {"type": "send_trip_update", "data": trip_data}
        )
        logger.debug(f"Mensaje enviado al grupo {TRIP_GROUP}: {trip_data}")
    except ValueError as e:
        logger.error(f"Serialization error for Trip {instance.id}: {str(e)}")
    except Exception as e:
        logger.exception(
            f"Unexpected error broadcasting Trip {instance.id} to {TRIP_GROUP}"
        )
