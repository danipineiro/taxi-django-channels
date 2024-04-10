from django.db import models

from common.models import TimeStampedModel


class Trip(TimeStampedModel):

    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    STARTED = 'started'
    COMPLETED = 'completed'

    STATUS_CHOICES = (
        (REQUESTED, 'Requested'),
        (ACCEPTED, 'Accepted'),
        (STARTED, 'Started'),
        (COMPLETED, 'Completed'),
    )

    passenger = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='trips_as_driver')
    source_latitude = models.FloatField()
    source_longitude = models.FloatField()
    destination_latitude = models.FloatField()
    destination_longitude = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=REQUESTED)