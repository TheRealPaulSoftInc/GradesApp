from django.contrib import admin
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from accounts import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('auth-user/', views.UserAuthView.as_view(), name='auth-user'),
    path('user/', views.UserListView.as_view(), name='users'),
    path('user/<int:id>/', views.UserDetailView.as_view(), name='user-detail'),
    path('activate/<token>/', views.ActivationView.as_view(), name='activate'),
    path('resend/', views.ResendActivationTokenView.as_view(),
         name='resend-activation'),
]
