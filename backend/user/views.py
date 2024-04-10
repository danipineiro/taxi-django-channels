import logging

from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import RegisterUserSerializer, ProfileUserSerializer

logger = logging.getLogger(__name__)


class UserSignUpView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer


class UserProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = ProfileUserSerializer(user)
        return Response(serializer.data)
