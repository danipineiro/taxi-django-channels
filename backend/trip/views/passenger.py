from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from trip.models import Trip
from trip.serializers import TripSerializer
from user.permissions import IsPassenger


class PassengerTripViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    A viewset for listing and retrieving trips for a driver.
    """

    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated, IsPassenger)
    lookup_field = "id"
    queryset = Trip.objects.all().order_by("-modified")

    def get_queryset(self):
        return self.queryset.filter(passenger=self.request.user)

    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != Trip.REQUESTED:
            raise ValidationError(
                f"You can only delete trips in the {Trip.REQUESTED} state."
            )
        return super().destroy(request, *args, **kwargs)
