import pytest
from rest_framework.test import APIClient
from django.urls import reverse

from budget.models import Budget, PlannedExpense, ExpenseCategory
from users.models import User


@pytest.fixture
def io_url():
    return reverse("budget:incomes_and_outcomes")


def test_io_user_not_authenticated_fail(client: APIClient, io_url):
    response = client.get(io_url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_io_without_budget_fail(user_client: APIClient, io_url):
    data = {"budget": 1, "date": "2020-01-01", "period": "MONTH"}
    response = user_client.get(io_url, data=data, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_io(user: User, client: APIClient, io_url):
    client.force_authenticate(user)
    User.save(user)
    family = user.person.family.first()
    budget = Budget.objects.create(name="test", description="test", family=family, period="MONTH")
    budget.refresh_from_db()
    expense_category = ExpenseCategory.objects.create(
        name="test", description="test", family=family
    )
    planned_expense = PlannedExpense.objects.create(
        amount=1000, category=expense_category, budget=budget
    )

    data = {"budget": budget.id, "date": "2020-01-01", "period": "MONTH"}
    response = client.get(io_url, data=data, format="json")
    print(response.data)
    assert response.status_code == 200
