from dj_rest_auth.views import (
    LoginView,
    LogoutView,
    UserDetailsView,
    PasswordResetView,
)
from django.urls import path, include
from rest_framework import routers

app_name = "users"

router = routers.DefaultRouter()

urlpatterns = [
    path("login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("me/", UserDetailsView.as_view(), name="me"),
    path("password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path("", include(router.urls)),
]