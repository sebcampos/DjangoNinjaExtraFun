
from django.urls import path
from . import views


urlpatterns = [
    path("video/live/", views.stream, name="stream"),
]
