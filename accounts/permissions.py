from django.contrib.auth import get_user_model
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit and retrieve it.
    Assumes the model instance has an 'user' attribute.
    """

    def has_permission(self, request, view):
        return request.user.is_staff
