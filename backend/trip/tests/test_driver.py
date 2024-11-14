import pytest
from django.test.utils import CaptureQueriesContext, override_settings
from django.db import connection, reset_queries

from common.tests.utils import BaseTestAPI
from trip.models import Trip
from trip.tests.factories import TripFactory
from user.tests.factories import PassengerFactory, DriverFactory


@pytest.mark.django_db
class TestTripList(BaseTestAPI):

    def test_driver_lists_only_requested_or_own_trips(self):
        """
        Test that a driver can only list trips that are either requested or assigned to them.

        This test creates two passengers and two drivers.
        It then creates trips with different statuses and drivers.
        The test authenticates one of the drivers and makes a GET request to list trips.
        It verifies that the response contains only the trips that are either requested or assigned to the authenticated driver.

        Assertions:
        - The total number of trips created is 3.
        - The response status code is 200 (OK).
        - The response contains 2 trips.
        - Each trip in the response has a status of 'REQUESTED' or is assigned to the authenticated driver.
        """
        passenger = PassengerFactory()
        passenger_2 = PassengerFactory()
        driver = DriverFactory()
        driver_2 = DriverFactory()

        TripFactory(passenger=passenger, status=Trip.REQUESTED)
        TripFactory(passenger=passenger_2, status=Trip.ACCEPTED, driver=driver)
        TripFactory(passenger=passenger_2, status=Trip.ACCEPTED, driver=driver_2)

        assert Trip.objects.count() == 3

        self.authenticate_user(driver)
        response = self.client.get("/api/v1/trip/driver/")

        assert response.status_code == 200
        assert len(response.json()) == 2
        for trip in response.json():
            assert trip["status"] == Trip.REQUESTED or trip["driver"] == driver.email, (
                f"Unexpected trip found: status={trip['status']}, driver={trip['driver']}"
            )

    def test_trip_list_contains_correct_fields_for_driver(self):
        """
        Test that the trip list for a driver contains the correct fields.

        This test creates a driver and a passenger.
        It then creates a trip with status 'REQUESTED' for the passenger and assigns it to the driver.
        The test authenticates the driver and makes a GET request to list trips.
        It verifies that the response status is 200 (OK) and that the response contains the expected fields with correct values.

        Assertions:
        - The response status code is 200 (OK).
        - The response contains the expected fields.
        - The status of the trip in the response matches the created trip's status.
        - The passenger in the response matches the created passenger's email.
        - The driver in the response matches the created driver's email.
        """
        driver = DriverFactory()
        passenger = PassengerFactory()

        trip = TripFactory(passenger=passenger, status=Trip.ACCEPTED, driver=driver)
        assert Trip.objects.count() == 1

        self.authenticate_user(driver)
        response = self.client.get("/api/v1/trip/driver/")

        assert response.status_code == 200

        expected_fields = {"id", "status", "driver", "passenger", "created", "modified"}
        response_data = response.json()[0]

        assert expected_fields <= response_data.keys()
        assert response_data["status"] == trip.status
        assert response_data["passenger"] == passenger.email
        assert response_data["driver"] == driver.email

    def test_trip_list_queries_remain_constant_with_more_trips(self):
        """
        Test that the number of queries remains constant when more trips are added to the list.

        This test creates a driver and a passenger, and authenticates the driver.
        It then creates trips and captures the number of queries made when listing trips.
        The test verifies that the number of queries remains the same when more trips are added.

        Assertions:
        - The response status code is 200 (OK) for each GET request.
        - The number of trips in the response matches the number of trips created.
        - The number of queries remains constant when more trips are added.
        """
        driver = DriverFactory()
        passenger = PassengerFactory()
        self.authenticate_user(driver)

        TripFactory(driver=driver, passenger=passenger, status=Trip.ACCEPTED)
        with CaptureQueriesContext(connection) as queries_with_one_trip:
            response = self.client.get("/api/v1/trip/driver/")
            assert response.status_code == 200
            assert len(response.json()) == 1

        TripFactory(driver=driver, passenger=passenger, status=Trip.ACCEPTED)
        with CaptureQueriesContext(connection) as queries_with_two_trips:
            response = self.client.get("/api/v1/trip/driver/")
            assert response.status_code == 200
            assert len(response.json()) == 2

        num_queries_with_two_trips = len(queries_with_two_trips)

        TripFactory(driver=driver, passenger=passenger, status=Trip.ACCEPTED)
        with CaptureQueriesContext(connection) as queries_with_three_trips:
            response = self.client.get("/api/v1/trip/driver/")
            assert response.status_code == 200
            assert len(response.json()) == 3

        num_queries_with_three_trips = len(queries_with_three_trips)

        assert num_queries_with_two_trips == num_queries_with_three_trips, (
            f"Expected the same or fewer queries, but got {num_queries_with_two_trips} for two trips "
            f"and {num_queries_with_three_trips} for three trips."
        )
