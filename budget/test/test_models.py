import pytest
from budget.models import Income, Expense, ExpenseCategory
from users.models import User, Family


@pytest.mark.django_db
def test_create_expense_category():
    category = ExpenseCategory.objects.create(name="test")
    assert category.name == "test"


@pytest.mark.django_db
def test_create_expense(user: User):
    family: Family = user.person.family.first()
    category = ExpenseCategory.objects.create(name="test", description="test", family=family)
    expense = Expense.objects.create(
        name="expense",
        amount=100.05,
        date="2021-01-01",
        category=category,
        user=user,
        family=family,
    )
    assert expense.name == "expense"


@pytest.mark.django_db
def test_create_income(user: User):
    family: Family = user.person.family.first()
    income = Income.objects.create(
        name="income",
        amount=100.05,
        date="2021-01-01",
        user=user,
        family=family,
    )
    assert income.name == "income"
