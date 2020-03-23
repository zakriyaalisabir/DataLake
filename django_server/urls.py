"""
django_server URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

admin.autodiscover()

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('datalake_rest_apis.urls')),
]
