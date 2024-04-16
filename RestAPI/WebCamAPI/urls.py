
from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_view, name="login"),
    path("video/live/", views.stream, name="stream"),
    path("video/tracking/", views.tracking_view, name="tracking"),
    path("logout", views.logout_view, name="logout")
]
