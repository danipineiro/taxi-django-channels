import logging

from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver

from trip.channels import broadcast_trip_state
from trip.models import Trip

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Trip)
def notify_trip_update(sender, instance, created, **kwargs):
    """
    Signal triggered when a Trip instance is saved.
    Notifies the trip group about the updated instance.
    """
    action = "created" if created else "updated"
    logger.debug(f"Signal: Trip {instance.id} has been {action}")

    async_to_sync(broadcast_trip_state)(instance)
