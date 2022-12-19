from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from budget.models import ExpenseCategory, Expense
from budget.serializers import ExpenseCategorySerializer, ExpenseSerializer
from utils.permissions import IsFamilyMember


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
