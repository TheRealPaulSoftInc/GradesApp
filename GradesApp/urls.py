from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls.conf import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.documentation import include_docs_urls
from GradesApp.settings import DEBUG
from accounts.jwt import JWTAuthentication
from django.conf.urls.static import static

class HttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        if DEBUG:
            schema.schemes = ["http", "https"]
        else:
            schema.schemes = ["https"]
        return schema

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
    generator_class=HttpsSchemaGenerator,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/grades/', include('grades.urls')),
]


# if settings.DEBUG:  # this should be set, but we want to expose the docs for everyone
if True:
    urlpatterns += [
        path('admin/', admin.site.urls),
        path('swagger/', schema_view.with_ui('swagger',
                                             cache_timeout=0), name='schema-swagger-ui'),
        path('docs/', include_docs_urls(title='GradesApp API',
                                        description='API for GradesApp', permission_classes=[permissions.AllowAny, ],
                                        authentication_classes=[])),
        path('swagger.json/',
             schema_view.without_ui(cache_timeout=0), name='schema-json'),
    ]
