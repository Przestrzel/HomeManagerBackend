from rest_framework import routers
from django.urls import path, include

from budget.views import ExpenseCategoryCreateView

app_name = "budget"

router = routers.DefaultRouter()

urlpatterns = [
    path("expenses/create-category/", ExpenseCategoryCreateView.as_view(), name="expense-category-create"),
    path("expenses/list-categories/", ExpenseCategoryCreateView.as_view(), name="expense-category-list"),
    path("", include(router.urls)),
]
