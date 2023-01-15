import json
import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from budget.models import Budget, PlannedExpense, ExpenseCategory, Period
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
def test_io_expenses(user: User, client: APIClient, io_url):
    client.force_authenticate(user=user)
    family = user.person.family.first()
    budget = Budget.objects.create(name="test", description="test", family=family, period="MONTH")
    budget.refresh_from_db()
    category_name = "test"
    expense_category = ExpenseCategory.objects.create(
        name=category_name, description="test", family=family
    )
    PlannedExpense.objects.create(amount=1000, category=expense_category, budget=budget)
    second_category_name = "test2"
    second_expense_category = ExpenseCategory.objects.create(
        name=second_category_name, description="test", family=family
    )
    PlannedExpense.objects.create(amount=2000, category=second_expense_category, budget=budget)

    data = {
        "budget": budget.id,
        "date": "2020-01-01",
        "period": "MONTH",
        "family": family.id,
    }
    response = client.get(io_url, data=data, content_type="application/json")

    assert response.status_code == 200
    expected_data = {
        "revenue": 0,
        "expenses": {
            category_name: {
                "amount": 0,
                "plannedAmount": 1000,
            },
            second_category_name: {
                "amount": 0,
                "plannedAmount": 2000,
            },
        },
    }
    assert json.loads(response.content) == expected_data
