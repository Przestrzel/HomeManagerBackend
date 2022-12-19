from django.shortcuts import render
from rest_framework import viewsets

from budget.models import ExpenseCategory


# Create your views here.

class ExpenseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseCategory.objects.all()
    serializer_class = ExpenseCategorySerializer