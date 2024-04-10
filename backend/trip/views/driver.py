from django.db.models import Q
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trip.models import Trip
from trip.serializers import TripSerializer
from user.permissions import IsDriver


class DriverTripViewset(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    """
    A viewset for listing and retrieving trips for a driver.
    """
    serializer_class = TripSerializer
    permission_classes = (IsAuthenticated, IsDriver)
    lookup_field = 'id'
    queryset = Trip.objects.all()

    def get_queryset(self):
        return (self.queryset
                .select_related('driver', 'passenger')
                .filter(Q(status=Trip.REQUESTED) | Q(driver=self.request.user))
                )

    @action(detail=True, methods=['post'])
    def accept_trip(self, request, *args, **kwargs):
        trip = self.get_object()
        trip.status = Trip.ACCEPTED
        trip.driver = request.user
        trip.save()
        return Response({'status': 'Trip accepted'})

    @action(detail=True, methods=['post'])
    def start_trip(self, request, *args, **kwargs):
        trip = self.get_object()
        trip.status = Trip.STARTED
        trip.save()
        return Response({'status': 'Trip started'})

    @action(detail=True, methods=['post'])
    def complete_trip(self, request, *args, **kwargs):
        trip = self.get_object()
        trip.status = Trip.COMPLETED
        trip.save()
        return Response({'status': 'Trip completed'})
