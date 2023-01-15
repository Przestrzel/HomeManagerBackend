from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from budget.models import Expense, Income, PlannedExpense, ExpenseCategory, Budget


class BudgetFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("name")
    family = SubFactory("users.tests.factories.FamilyFactory")
    period = "MONTH"

    class Meta:
        model = Budget


class ExpenseCategoryFactory(DjangoModelFactory):
    name = Faker("name")
    description = Faker("name")
    family = SubFactory("users.tests.factories.FamilyFactory")

    class Meta:
        model = ExpenseCategory


class ExpensesFactory(DjangoModelFactory):
    name = Faker("name")
    amount = FuzzyInteger(500, 5000)
    date = Faker("date")
    category = SubFactory(ExpenseCategoryFactory)
    user = SubFactory("users.tests.factories.UserFactory")
    family = SubFactory("users.tests.factories.FamilyFactory")

    class Meta:
        model = Expense


class IncomeFactory(DjangoModelFactory):
    name = Faker("name")
    amount = FuzzyInteger(50, 25000)
    date = Faker("date")
    user = SubFactory("users.tests.factories.UserFactory")
    family = SubFactory("users.tests.factories.FamilyFactory")

    class Meta:
        model = Income


class PlannedExpenseFactory(DjangoModelFactory):
    amount = Faker("pydecimal", left_digits=10, right_digits=2, positive=True)
    category = SubFactory(ExpenseCategoryFactory)
    budget = SubFactory(BudgetFactory)

    class Meta:
        model = PlannedExpense
