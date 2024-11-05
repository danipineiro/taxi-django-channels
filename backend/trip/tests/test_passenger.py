import pytest
from django.test.utils import CaptureQueriesContext
from django.db import connection

from common.tests.utils import BaseTestAPI
from trip.models import Trip
from trip.tests.factories import TripFactory
from user.tests.factories import PassengerFactory, DriverFactory


@pytest.mark.django_db
class TestTripCreation(BaseTestAPI):

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

    def test_passenger_trip_creation_returns_correct_fields(self):
        user = PassengerFactory()
        self.authenticate_user(user)

        response = self.client.post("/api/v1/trip/passenger/")

        assert response.status_code == 201

        expected_fields = {"id", "status", "driver", "passenger", "created", "modified"}
        response_data = response.json()

        assert expected_fields <= response_data.keys()
        assert response_data["status"] == Trip.REQUESTED
        assert response_data["passenger"] == user.email
        assert response_data["driver"] is None


@pytest.mark.django_db
class TestTripList(BaseTestAPI):

    def test_passenger_cannot_list_other_passenger_trips(self):
        user = PassengerFactory()
        user_2 = PassengerFactory()

        trip = TripFactory(passenger=user)
        trip_2 = TripFactory(passenger=user_2)

        assert Trip.objects.count() == 2

        self.authenticate_user(user)
        response = self.client.get("/api/v1/trip/passenger/")

        assert response.status_code == 200
        assert len(response.json()) == 1
        for trip in response.json():
            assert trip["passenger"] == user.email

    def test_passenger_list_trips_correct_fields(self):
        user = PassengerFactory()
        self.authenticate_user(user)

        trip = TripFactory(passenger=user)

        response = self.client.get("/api/v1/trip/passenger/")

        assert response.status_code == 200

        expected_fields = {"id", "status", "driver", "passenger", "created", "modified"}
        response_data = response.json()[0]

        assert expected_fields <= response_data.keys()
        assert response_data["status"] == trip.status
        assert response_data["passenger"] == user.email
        assert response_data["driver"] is None

    def test_trip_list_queries_remain_constant_with_more_trips(self):
        """
        Test that the number of database queries remains constant when listing trips,
        even as the number of trips increases.

        This test ensures that the query count does not increase linearly with the number
        of trips, which would indicate a potential performance issue.
        """
        user = PassengerFactory()
        self.authenticate_user(user)

        TripFactory(passenger=user)

        with CaptureQueriesContext(connection) as queries_with_one_trip:
            response = self.client.get("/api/v1/trip/passenger/")
            assert response.status_code == 200
            assert len(response.json()) == 1

        num_queries_with_one_trip = len(queries_with_one_trip)

        TripFactory(passenger=user)

        with CaptureQueriesContext(connection) as queries_with_two_trips:
            response = self.client.get("/api/v1/trip/passenger/")
            assert response.status_code == 200
            assert len(response.json()) == 2

        num_queries_with_two_trips = len(queries_with_two_trips)

        assert num_queries_with_two_trips <= num_queries_with_one_trip, (
            f"Expected the same or fewer queries, but got {num_queries_with_one_trip} for one trip "
            f"and {num_queries_with_two_trips} for two trips."
        )
