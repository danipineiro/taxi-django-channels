from rest_framework import serializers

from trip.models import Trip


class TripSerializer(serializers.ModelSerializer):
    driver = serializers.SerializerMethodField()
    passenger = serializers.SerializerMethodField()

    class Meta:
        model = Trip
        fields = (
            "id",
            "source_latitude",
            "source_longitude",
            "destination_latitude",
            "destination_longitude",
            "status",
            "driver",
            "passenger",
        )
        read_only_fields = ("id", "status", "driver", "passenger")

    def get_driver(self, obj):
        if obj.driver is None:
            return None

        return obj.driver.email

    def get_passenger(self, obj):
        return obj.passenger.email
