import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.tests.factories import PassengerFactory, DriverFactory


@pytest.mark.django_db
def test_passenger_can_create_trip():
    user = PassengerFactory()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/api/v1/trip/passenger/")

    assert response.status_code == 201


@pytest.mark.django_db
def test_driver_can_not_create_trip():
    user = DriverFactory()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    response = client.post("/api/v1/trip/passenger/")

    assert response.status_code == 403

