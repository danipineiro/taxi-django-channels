from rest_framework.routers import DefaultRouter

from trip.views import PassengerTripViewset, DriverTripViewset

router = DefaultRouter()

router.register(r'trip/passenger', PassengerTripViewset, basename='trip-passenger')
router.register(r'trip/driver', DriverTripViewset, basename='trip-driver')

urlpatterns = router.urls
