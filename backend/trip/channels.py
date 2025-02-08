import logging

from channels.layers import get_channel_layer

from trip.constants import TRIP_GROUP
from trip.serializers import TripSerializer

logger = logging.getLogger(__name__)


async def broadcast_trip_state(instance):
    """
    Broadcasts trip update to the specified group using Django Channels.
    """
    channel_layer = get_channel_layer()
    if not channel_layer:
        logger.warning(
            f"Channel layer not configured. Skipping broadcast for Trip ID {instance.id}."
        )
        return

    trip_data = TripSerializer(instance).data

    try:
        await channel_layer.group_send(
            TRIP_GROUP, {"type": "send_trip_update", "data": trip_data}
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
