from django.db import models

from common.models import TimeStampedModel


class Trip(TimeStampedModel):

    REQUESTED = "requested"
    ACCEPTED = "accepted"
    STARTED = "started"
    COMPLETED = "completed"

    STATUS_CHOICES = (
        (REQUESTED, "Requested"),
        (ACCEPTED, "Accepted"),
        (STARTED, "Started"),
        (COMPLETED, "Completed"),
    )

    passenger = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="trips"
    )
    driver = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        related_name="trips_as_driver",
        null=True,
        blank=True,
    )
    source_latitude = models.FloatField(null=True, blank=True)
    source_longitude = models.FloatField(null=True, blank=True)
    destination_latitude = models.FloatField(null=True, blank=True)
    destination_longitude = models.FloatField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)
