from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from trip.models import Trip
from trip.serializers import TripSerializer
from user.permissions import IsPassenger


class PassengerTripViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset for listing and retrieving trips for a driver.
    """

    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated, IsPassenger)
    lookup_field = "id"
    queryset = Trip.objects.all()

    def get_queryset(self):
        return self.queryset.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)
