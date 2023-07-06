from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordResetView,
)
from dj_rest_auth.jwt_auth import get_refresh_view
from django.urls import path, include
from rest_framework import routers

app_name = "users"

router = routers.DefaultRouter()

urlpatterns = [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("refresh/", get_refresh_view().as_view(), name="refresh_token"),
    path("me/", UserDetailsView.as_view(), name="me"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("", include(router.urls)),
]
