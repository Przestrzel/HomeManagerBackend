from factory import Faker
from factory.django import DjangoModelFactory

from budget.models import Expense, Income


class ExpensesFactory(DjangoModelFactory):
    class Meta:
        model = Expense


class IncomeFactory(DjangoModelFactory):
    class Meta:
        model = Income
