from django.contrib.auth import get_user_model
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit and retrieve it.
    Assumes the model instance has an 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsCourseOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a Course to edit and retrieve it.
    Assumes the model instance has an 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.semester.user == request.user


class IsGradeOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of a Grade to edit and retrieve it.
    Assumes the model instance has an 'user' attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.course.semester.user == request.user
