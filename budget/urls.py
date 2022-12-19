from rest_framework import routers
from django.urls import path, include

app_name = "budget"

router = routers.DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
]
