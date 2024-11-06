import pytest
from django.test.utils import CaptureQueriesContext, override_settings
from django.db import connection, reset_queries

from common.tests.utils import BaseTestAPI
from trip.models import Trip
from trip.tests.factories import TripFactory
from user.tests.factories import PassengerFactory, DriverFactory


@pytest.mark.django_db
class TestTripCreation(BaseTestAPI):

    def test_passenger_can_create_trip(self):
        """
        Test that a passenger can create a trip.

        This test creates a passenger and authenticates them.
        It then makes a POST request to create a trip and verifies that the response status is 201 (Created).

        Assertions:
        - The response status code is 201 (Created).
        """
        user = PassengerFactory()
        self.authenticate_user(user)

        response = self.client.post("/api/v1/trip/passenger/")

        assert response.status_code == 201

    def test_driver_cannot_create_trip(self):
        """
        Test that a driver cannot create a trip.

        This test creates a driver and authenticates them.
        It then makes a POST request to create a trip and verifies that the response status is 403 (Forbidden).

        Assertions:
        - The response status code is 403 (Forbidden).
        """
        user = DriverFactory()
        self.authenticate_user(user)

        response = self.client.post("/api/v1/trip/passenger/")

        assert response.status_code == 403

    def test_passenger_trip_creation_returns_correct_fields(self):
        """
        Test that the trip creation for a passenger returns the correct fields.

        This test creates a passenger and authenticates them.
        It then makes a POST request to create a trip and verifies that the response status is 201 (Created).
        The test also checks that the response contains the expected fields with correct values.

        Assertions:
        - The response status code is 201 (Created).
        - The response contains the expected fields.
        - The status of the trip in the response is 'REQUESTED'.
        - The passenger in the response matches the authenticated passenger.
        - The driver in the response is None.
        """
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
        """
        Test that a passenger cannot list trips of other passengers.

        This test creates two passengers and two trips, one for each passenger.
        It then authenticates the first passenger and makes a GET request to list trips.
        The test verifies that only the trip of the authenticated passenger is returned.

        Assertions:
        - The total number of trips in the database is 2.
        - The response status code is 200 (OK).
        - The response contains only one trip.
        - The trip in the response belongs to the authenticated passenger.
        """
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
        """
        Test that the trip list for a passenger contains the correct fields.

        This test creates a passenger and a trip for that passenger.
        It then authenticates the passenger and makes a GET request to list trips.
        The test verifies that the response status is 200 and that the response
        contains the expected fields with correct values.

        Assertions:
        - The response status code is 200 (OK).
        - The response contains the expected fields.
        - The status of the trip in the response matches the created trip.
        - The passenger in the response matches the authenticated passenger.
        - The driver in the response is None.
        """
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

        TripFactory(passenger=user)
        with CaptureQueriesContext(connection) as queries_with_two_trips:
            response = self.client.get("/api/v1/trip/passenger/")
            assert response.status_code == 200
            assert len(response.json()) == 2

        num_queries_with_two_trips = len(queries_with_two_trips)

        TripFactory(passenger=user)
        with CaptureQueriesContext(connection) as queries_with_three_trips:
            response = self.client.get("/api/v1/trip/passenger/")
            assert response.status_code == 200
            assert len(response.json()) == 3

        num_queries_with_three_trips = len(queries_with_three_trips)

        assert num_queries_with_two_trips == num_queries_with_three_trips, (
            f"Expected the same or fewer queries, but got {num_queries_with_two_trips} for two trips "
            f"and {num_queries_with_three_trips} for three trips."
        )


@pytest.mark.django_db
class TestTripDeletion(BaseTestAPI):

    def test_passenger_delete_requested_trip(self):
        """
        Test that a passenger can delete a trip with status 'REQUESTED'.

        This test creates a passenger and a trip with status 'REQUESTED' for that passenger.
        It then authenticates the passenger and makes a DELETE request to delete the trip.
        The test verifies that the response status is 204 (No Content).

        Assertions:
        - The response status code is 204 (No Content).
        """
        user = PassengerFactory()
        self.authenticate_user(user)

        trip = TripFactory(passenger=user, status=Trip.REQUESTED)
        response = self.client.delete(f"/api/v1/trip/passenger/{trip.id}/")
        assert response.status_code == 204

    def test_passenger_cannot_delete_non_requested_trip(self):
        """
        Test that a passenger cannot delete a trip if its status is different from 'REQUESTED'.

        This test creates a passenger and authenticates them.
        It then creates trips with different statuses ('ACCEPTED', 'STARTED', 'COMPLETED') for that passenger.
        For each trip, it makes a DELETE request and verifies that the response status is 400 (Bad Request).

        Assertions:
        - The response status code is 400 (Bad Request) for trips with status 'ACCEPTED'.
        - The response status code is 400 (Bad Request) for trips with status 'STARTED'.
        - The response status code is 400 (Bad Request) for trips with status 'COMPLETED'.
        """
        user = PassengerFactory()
        self.authenticate_user(user)

        trip = TripFactory(passenger=user, status=Trip.ACCEPTED)
        response = self.client.delete(f"/api/v1/trip/passenger/{trip.id}/")
        assert response.status_code == 400

        trip = TripFactory(passenger=user, status=Trip.STARTED)
        response = self.client.delete(f"/api/v1/trip/passenger/{trip.id}/")
        assert response.status_code == 400

        trip = TripFactory(passenger=user, status=Trip.COMPLETED)
        response = self.client.delete(f"/api/v1/trip/passenger/{trip.id}/")
        assert response.status_code == 400
