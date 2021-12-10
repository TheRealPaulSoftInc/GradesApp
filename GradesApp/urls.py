from django.contrib import admin
from django.urls import include, path
from django.urls.conf import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.documentation import include_docs_urls
from accounts.jwt import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title='GradesApp API',
        default_version='v1',
        description='API for GradesApp',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="paulsoftinc@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[]
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/grades/', include('grades.urls')),
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', include_docs_urls(title='GradesApp API',
         description='API for GradesApp', permission_classes=[permissions.AllowAny, ],
                                    authentication_classes=[])),
    path('swagger.json/',
         schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
