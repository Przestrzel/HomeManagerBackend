from factory import Faker
from factory.django import DjangoModelFactory
from budget.models import ExpenseCategory


class ExpenseCategoryFactory(DjangoModelFactory):
    name = Faker("name")

    class Meta:
        model = ExpenseCategory
