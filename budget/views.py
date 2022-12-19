from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from budget.models import ExpenseCategory
from budget.serializers import ExpenseCategorySerializer
from utils.permissions import IsFamilyMember


class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer
    permission_classes = [IsAuthenticated, IsFamilyMember]
    pagination_class = None
