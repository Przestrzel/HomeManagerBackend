from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from budget.models import ExpenseCategory, Expense, Income, Budget, PlannedExpense
from budget.serializers import ExpenseCategorySerializer, ExpenseSerializer, IncomeSerializer, ExpenseCreateSerializer, \
    IncomeCreateSerializer, BudgetSerializer, PlannedExpenseSerializer, PlannedExpenseCreateSerializer
from utils.permissions import IsFamilyMember


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_classes = {
        "list": ExpenseSerializer,
        "retrieve": ExpenseSerializer,
        "create": ExpenseCreateSerializer,
        "update": ExpenseSerializer
    }
    default_serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def check_permissions(self, request):
        if request.method == "DELETE":
            self.permission_classes = [IsAuthenticated]
        super().check_permissions(request)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_destroying_own_expense = request.user.family.filter(id=instance.family.id).exists()
        if not is_destroying_own_expense:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_classes = {
        "list": IncomeSerializer,
        "retrieve": IncomeSerializer,
        "create": IncomeCreateSerializer,
        "update": IncomeSerializer
    }
    default_serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        is_destroying_own_expense = request.user.family.filter(id=instance.family.id).exists()
        if not is_destroying_own_expense:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None


class PlannedExpenseViewSet(viewsets.ModelViewSet):
    queryset = PlannedExpense.objects.all()
    serializer_classes = {
        "list": PlannedExpenseSerializer,
        "retrieve": PlannedExpenseSerializer,
        "create": PlannedExpenseCreateSerializer,
        "update": PlannedExpenseSerializer
    }
    default_serializer_class = PlannedExpenseSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer_class)
