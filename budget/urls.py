from rest_framework import routers
from django.urls import path, include

from budget.views import ExpenseCategoryViewSet

app_name = "budget"

router = routers.DefaultRouter()

urlpatterns = [
    path("expenses/categories/", ExpenseCategoryViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name="expense-categories"),
    path("", include(router.urls)),
]
