from rest_framework import permissions

from user.models import User


class IsDriver(permissions.BasePermission):
    """
    Custom permission to only allow drivers to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a driver
        return request.user.is_authenticated and request.user.type == User.DRIVER


class IsPassenger(permissions.BasePermission):
    """
    Custom permission to only allow passengers to access the view.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a passenger
        return request.user.is_authenticated and request.user.type == User.PASSENGER
