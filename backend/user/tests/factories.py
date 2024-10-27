import factory
from faker import Faker

from user.models import User

faker = Faker()


class PassengerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.email())
    type = User.PASSENGER


class DriverFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.email())
    type = User.DRIVER
