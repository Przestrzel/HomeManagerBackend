from factory import Faker
from factory.django import DjangoModelFactory

from budget.models import Expense, Income, PlannedExpense, ExpenseCategory


class ExpensesFactory(DjangoModelFactory):
    class Meta:
        model = Expense


class IncomeFactory(DjangoModelFactory):
    class Meta:
        model = Income


class PlannedExpenseFactory(DjangoModelFactory):
    class Meta:
        model = PlannedExpense


class ExpenseCategoryFactory(DjangoModelFactory):
    class Meta:
        model = ExpenseCategory
