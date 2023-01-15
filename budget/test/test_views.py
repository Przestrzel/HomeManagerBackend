import json
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from budget.models import Budget, PlannedExpense
from budget.test.factories import (
    BudgetFactory,
    ExpenseCategoryFactory,
    PlannedExpenseFactory,
    IncomeFactory,
    ExpensesFactory,
)
from users.models import User, Family


@pytest.fixture
def io_url():
    return reverse("budget:incomes_and_outcomes")


def test_io_user_not_authenticated_fail(client: APIClient, io_url):
    response = client.get(io_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_io_user_not_in_family_fail(user_client: APIClient, io_url):
    response = user_client.get(io_url, data={"family": -1})
    assert response.status_code == 403


@pytest.mark.django_db
def test_io_without_budget_fail(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first().id
    data = {"date": "2020-01-01", "period": "MONTH", "family": family}
    response = client.get(io_url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_io_planned_expenses_count_to_proper_category(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = BudgetFactory(family=family)
    expense_category = ExpenseCategoryFactory(family=family)
    second_expense_category = ExpenseCategoryFactory(family=family)
    planned_expense = PlannedExpenseFactory(budget=budget, category=expense_category, amount=1000)
    second_planned_expense = PlannedExpenseFactory(
        budget=budget, category=second_expense_category, amount=2000
    )

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")

    assert response.status_code == 200
    expected_data = {
        "income": 0,
        "expenses": {
            expense_category.name: {
                "amount": 0,
                "plannedAmount": planned_expense.amount,
            },
            second_expense_category.name: {
                "amount": 0,
                "plannedAmount": second_planned_expense.amount,
            },
        },
    }
    assert json.loads(response.content) == expected_data


@pytest.mark.django_db
def test_io_income_count_in_one_month(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = BudgetFactory(family=family)
    IncomeFactory(amount=1000, date="2020-01-01", user=user, family=family)
    IncomeFactory(amount=3000, date="2020-01-15", user=user, family=family)
    IncomeFactory(amount=2500, date="2020-01-31", user=user, family=family)

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")
    expected_data = {
        "income": 6500,
        "expenses": {},
    }

    assert response.status_code == 200
    assert json.loads(response.content) == expected_data


@pytest.mark.django_db
def test_io_income_count_in_different_month_dont_calculate(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = BudgetFactory(family=family)

    IncomeFactory(amount=1000, date="2020-01-01", user=user, family=family)
    IncomeFactory(amount=1000, date="2020-01-31", user=user, family=family)
    IncomeFactory(amount=3000, date="2020-01-03", user=user, family=family)
    IncomeFactory(amount=2500, date="2020-01-28", user=user, family=family)

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")
    expected_data = {
        "income": 7500,
        "expenses": {},
    }

    assert response.status_code == 200
    assert json.loads(response.content) == expected_data


@pytest.mark.django_db
def test_io_expenses_in_different_category_properly_assigns(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = BudgetFactory(family=family)
    expense_category = ExpenseCategoryFactory(family=family)
    second_expense_category = ExpenseCategoryFactory(family=family)
    ExpensesFactory(
        amount=1000, date="2020-01-01", user=user, family=family, category=expense_category
    )
    ExpensesFactory(
        amount=200, date="2020-01-31", user=user, family=family, category=second_expense_category
    )
    ExpensesFactory(
        amount=800, date="2020-01-15", user=user, family=family, category=expense_category
    )
    ExpensesFactory(
        amount=300, date="2020-01-07", user=user, family=family, category=second_expense_category
    )

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")
    expected_data = {
        "income": 0,
        "expenses": {
            expense_category.name: {
                "amount": 1800,
                "plannedAmount": 0,
            },
            second_expense_category.name: {
                "amount": 500,
                "plannedAmount": 0,
            },
        },
    }

    assert response.status_code == 200
    assert json.loads(response.content) == expected_data


@pytest.mark.django_db
def test_io_expenses_and_planned_dont_disturb_other(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = BudgetFactory(family=family)
    expense_category = ExpenseCategoryFactory(family=family)
    second_expense_category = ExpenseCategoryFactory(family=family)
    ExpensesFactory(
        amount=1000, date="2020-01-01", user=user, family=family, category=expense_category
    )
    ExpensesFactory(
        amount=200, date="2020-01-31", user=user, family=family, category=second_expense_category
    )
    ExpensesFactory(
        amount=800, date="2020-01-15", user=user, family=family, category=expense_category
    )
    ExpensesFactory(
        amount=300, date="2020-01-07", user=user, family=family, category=second_expense_category
    )
    PlannedExpenseFactory(budget=budget, category=expense_category, amount=1000)
    PlannedExpenseFactory(budget=budget, category=second_expense_category, amount=2000)

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")
    expected_data = {
        "income": 0,
        "expenses": {
            expense_category.name: {
                "amount": 1800,
                "plannedAmount": 1000,
            },
            second_expense_category.name: {
                "amount": 500,
                "plannedAmount": 2000,
            },
        },
    }

    assert response.status_code == 200
    assert json.loads(response.content) == expected_data
