from django.urls import path, include
from rest_framework import routers

from budget.views import (
    ExpenseCategoryViewSet,
    ExpenseViewSet,
    IncomeViewSet,
    BudgetViewSet,
    PlannedExpenseViewSet,
    get_incomes_and_outcomes,
)

app_name = "budget"

router = routers.DefaultRouter()
router.register(r"expenses/categories", ExpenseCategoryViewSet, basename="expense-category")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"incomes", IncomeViewSet, basename="income")
router.register(r"plan-expenses", PlannedExpenseViewSet, basename="planned-expense")
router.register(r"", BudgetViewSet, basename="budget")

urlpatterns = [
    path("incomes-and-outcomes/", get_incomes_and_outcomes, name="incomes_and_outcomes"),
    path("", include(router.urls)),
]
