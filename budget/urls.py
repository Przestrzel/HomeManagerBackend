from rest_framework import routers
from django.urls import path, include

from budget.views import ExpenseCategoryViewSet, ExpenseViewSet

app_name = "budget"

router = routers.DefaultRouter()
router.register(r"expenses/categories", ExpenseCategoryViewSet)
router.register(r"expenses", ExpenseViewSet)

urlpatterns = router.urls
