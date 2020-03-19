from django.urls import path

from .views import DatalakeViews

urlpatterns = [
    path(r'', DatalakeViews.as_view())
]
