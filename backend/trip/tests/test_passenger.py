import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.tests.factories import PassengerFactory, DriverFactory


@pytest.mark.django_db
class TestTripCreation:
    def setup_method(self):
        self.client = APIClient()

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    def test_passenger_can_create_trip(self):
        user = PassengerFactory()
        self.authenticate_user(user)

        response = self.client.post("/api/v1/trip/passenger/")

        assert response.status_code == 201

    def test_driver_cannot_create_trip(self):
        user = DriverFactory()
        self.authenticate_user(user)

        response = self.client.post("/api/v1/trip/passenger/")

        assert response.status_code == 403
