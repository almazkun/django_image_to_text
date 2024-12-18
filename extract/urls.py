from django.urls import path

from extract.views import ExtractView

urlpatterns = [
    path("", ExtractView.as_view(), name="extract"),
]
