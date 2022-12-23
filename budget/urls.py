from rest_framework import routers

from budget.views import ExpenseCategoryViewSet, ExpenseViewSet, IncomeViewSet

app_name = "budget"

router = routers.DefaultRouter()
router.register(r"expenses/categories", ExpenseCategoryViewSet)
router.register(r"expenses", ExpenseViewSet)
router.register(r"incomes", IncomeViewSet)

urlpatterns = router.urls
