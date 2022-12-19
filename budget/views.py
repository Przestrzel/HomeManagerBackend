from rest_framework import viewsets
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from budget.models import ExpenseCategory
from budget.serializers import ExpenseCategorySerializer
from utils.permissions import IsFamilyMember


class ExpenseCategoryCreateView(CreateAPIView):
    model = ExpenseCategory
    permission_classes = [IsAuthenticated, IsFamilyMember]
    serializer_class = ExpenseCategorySerializer
    queryset = ExpenseCategory.objects.all()
