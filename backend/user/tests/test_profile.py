import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from user.tests.factories import PassengerFactory


@pytest.mark.django_db
def test_profile_endpoint():
    """
    Test the profile endpoint with a valid JWT token.

    This test verifies that the profile endpoint returns the correct user data
    when accessed with a valid JWT token.

    Steps:
    1. Create a user using the PassengerFactory.
    2. Generate a JWT token for the created user.
    3. Set the JWT token in the API client's authorization header.
    4. Send a GET request to the profile endpoint.
    5. Assert that the response status code is 200.
    6. Assert that the response data contains the correct email address.

    Assertions:
    - The response status code should be 200.
    - The email in the response data should match the user's email.
    """
    user = PassengerFactory()
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    response = client.get("/api/v1/profile/")

    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_profile_endpoint_without_jwt():
    """
    Test the profile endpoint without a JWT token.

    This test verifies that the profile endpoint returns a 404 status code
    when accessed without a JWT token.

    Steps:
    1. Initialize the API client without setting any authorization headers.
    2. Send a GET request to the profile endpoint.
    3. Assert that the response status code is 404.

    Assertions:
    - The response status code should be 404.
    """
    client = APIClient()
    response = client.get("/api/profile/")

    assert response.status_code == 404
