import logging

from channels.layers import get_channel_layer

from trip.constants import TRIP_GROUP, DRIVERS_GROUP
from trip.serializers import TripSerializer

logger = logging.getLogger(__name__)


async def broadcast_trip_state(instance, created=False):
    """
    Broadcasts trip update to the specified group using Django Channels.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.warning(
            f"Channel layer not configured. Skipping broadcast for Trip ID {instance.id}."
        )
        return

    try:
        trip_data = TripSerializer(instance).data

        group = DRIVERS_GROUP if created else TRIP_GROUP

        await channel_layer.group_send(
            group, {"type": "send_trip_update", "data": trip_data}
        )
        logger.debug(
            f"Trip update broadcasted successfully. Trip ID: {instance.id}, Group: {TRIP_GROUP}, Data: {trip_data}"
        )
    except ValueError as e:
        logger.error(f"Serialization error for Trip ID {instance.id}. Error: {str(e)}")
    except Exception as e:
        logger.exception(
            f"Unexpected error broadcasting Trip ID {instance.id} to Group {TRIP_GROUP}.",
            exc_info=True,
        )


async def send_trip_deleted(instance_id):
    """
    Broadcasts trip deletion to the specified group using Django Channels.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.warning(
            f"Channel layer not configured. Skipping broadcast for Trip ID {instance_id}."
        )
        return

    try:
        await channel_layer.group_send(
            TRIP_GROUP, {"type": "send_trip_deleted", "data": {"id": instance_id}}
        )
        logger.debug(
            f"Trip deletion broadcasted successfully. Trip ID: {instance_id}, Group: {TRIP_GROUP}"
        )
    except Exception as e:
        logger.exception(
            f"Unexpected error broadcasting Trip ID {instance_id} deletion to Group {TRIP_GROUP}.",
            exc_info=True,
        )
