from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class BaseTestAPI:
    def setup_method(self):
        self.client = APIClient()

    def authenticate_user(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
