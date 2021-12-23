from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from grades.models import Course, Grade, Semester
from grades.permissions import IsCourseOwner, IsGradeOwner, IsOwner
from grades.serializers import (CourseSerializer, GradeSerializer,
                                SemesterSerializer)


class SemesterView(ListCreateAPIView):
    """
    get: List all Semesters of the authenticated user.
    post: Creates new Semester.
    """

    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated, IsOwner, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['order']

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user)


class SemesterDetailView(RetrieveUpdateDestroyAPIView):
    """
    get: Retrieves a User's Semester by Id
    put: Updates a Semester by Id
    delete: Deletes a Semester by Id
    """

    http_method_names = ['get', 'put', 'delete']
    serializer_class = SemesterSerializer
    permission_classes = [IsAuthenticated, IsOwner, DjangoModelPermissions]
    lookup_field = 'id'

    def get_queryset(self):
        return Semester.objects.filter(user=self.request.user)


class CourseView(ListCreateAPIView):
    """
    get: List all Courses of the authenticated user.
    post: Creates new Course.
    """

    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCourseOwner, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['order']

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Course.objects.filter(semester__user=self.request.user)


class CourseDetailView(RetrieveUpdateDestroyAPIView):
    """
    get: Retrieves a User's Course by Id
    put: Updates a Course by Id
    delete: Deletes a Course by Id
    """

    http_method_names = ['get', 'put', 'delete']
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated, IsCourseOwner, DjangoModelPermissions]
    lookup_field = 'id'

    def get_queryset(self):
        return Course.objects.filter(semester__user=self.request.user)


class GradeView(ListCreateAPIView):
    """
    get: List all Grades of the authenticated user.
    post: Creates new Grade.
    """

    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsGradeOwner, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = '__all__'
    search_fields = '__all__'
    ordering_fields = '__all__'
    ordering = ['order']

    def perform_create(self, serializer):
        return serializer.save()

    def get_queryset(self):
        return Grade.objects.filter(course__semester__user=self.request.user)


class GradeDetailView(RetrieveUpdateDestroyAPIView):
    """
    get: Retrieves a User's Grade by Id
    put: Updates a Grade by Id
    delete: Deletes a Grade by Id
    """

    http_method_names = ['get', 'put', 'delete']
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated, IsGradeOwner, DjangoModelPermissions]
    lookup_field = 'id'

    def get_queryset(self):
        return Grade.objects.filter(course__semester__user=self.request.user)
