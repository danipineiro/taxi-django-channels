import factory
from faker import Faker

from trip.models import Trip

faker = Faker()


class TripFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Trip
