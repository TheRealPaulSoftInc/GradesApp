from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from grades import views

app_name = 'grades'
urlpatterns = [
    path('semester/', views.SemesterView.as_view(), name='semesters'),
    path('semester/<int:id>/', views.SemesterDetailView.as_view(),
         name='semester-detail'),
    path('course/', views.CourseView.as_view(), name='courses'),
    path('course/<int:id>/', views.CourseDetailView.as_view(),
         name='course-detail'),
    path('grade/', views.GradeView.as_view(), name='grades'),
    path('grade/<int:id>/', views.GradeDetailView.as_view(),
         name='grade-detail'),
]
