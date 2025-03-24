import logging

from channels.layers import get_channel_layer

from trip.constants import DRIVERS_GROUP, TRIP_GROUP
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
    except ValueError as e:
        logger.error(f"Serialization error for Trip ID {instance.id}. Error: {str(e)}")
        return

    if created:
        try:
            await channel_layer.group_send(
                DRIVERS_GROUP, {"type": "send_trip_update", "data": trip_data}
            )
            logger.debug(
                f"Trip update broadcasted successfully. Trip ID: {instance.id}, Group: {DRIVERS_GROUP}, Data: {trip_data}"
            )
        except Exception as e:
            logger.exception(
                f"Unexpected error broadcasting Trip ID {instance.id} to Group {DRIVERS_GROUP}.",
                exc_info=True,
            )
    else:
        try:
            await channel_layer.group_send(
                instance.passenger_id, {"type": "send_trip_update", "data": trip_data}
            )
            logger.debug(
                f"Trip update broadcasted successfully. Trip ID: {instance.id}, Group: {instance.passenger_id}, Data: {trip_data}"
            )
        except Exception as e:
            logger.exception(
                f"Unexpected error broadcasting Trip ID {instance.id} to Group {instance.passenger_id}.",
                exc_info=True,
            )
        try:
            await channel_layer.group_send(
                instance.driver_id, {"type": "send_trip_update", "data": trip_data}
            )
            logger.debug(
                f"Trip update broadcasted successfully. Trip ID: {instance.id}, Group: {instance.driver_id}, Data: {trip_data}"
            )
        except Exception as e:
            logger.exception(
                f"Unexpected error broadcasting Trip ID {instance.id} to Group {instance.driver_id}.",
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
