from IPython.core.display_functions import update_display
from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trip.models import Trip
from trip.serializers import TripSerializer
from user.permissions import IsDriver


class DriverTripViewset(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """
    A viewset for listing and retrieving trips for a driver.
    """

    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated, IsDriver)
    lookup_field = "id"
    queryset = Trip.objects.all().order_by("-modified")

    def get_queryset(self):
        return self.queryset.select_related("driver", "passenger").filter(
            Q(status=Trip.REQUESTED) | Q(driver=self.request.user)
        )

    @action(detail=True, methods=["post"])
    def accept(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.status != Trip.REQUESTED:
            return Response(
                {"status": "Trip has already been accepted or is not requested"},
                status=400,
            )
        trip.status = Trip.ACCEPTED
        trip.driver = request.user
        trip.save(update_fields=["status", "driver"])
        return Response({"status": "Trip accepted"})

    @action(detail=True, methods=["post"])
    def start(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.status != Trip.ACCEPTED:
            return Response(
                {
                    "status": "Trip has not been accepted yet or has already been started"
                },
                status=400,
            )
        trip.status = Trip.STARTED
        trip.save(update_fields=["status"])
        return Response({"status": "Trip started"})

    @action(detail=True, methods=["post"])
    def complete(self, request, *args, **kwargs):
        trip = self.get_object()
        if trip.status != Trip.STARTED:
            return Response(
                {
                    "status": "Trip has not been started yet or has already been completed"
                },
                status=400,
            )
        trip.status = Trip.COMPLETED
        trip.save(update_fields=["status"])
        return Response({"status": "Trip completed"})
