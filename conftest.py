import pytest
from rest_framework.test import APIClient
from users.models import User
from users.tests.factories import UserFactory, FamilyFactory


@pytest.fixture
def user() -> User:
    family = FamilyFactory()
    ret_user: User = UserFactory.create(person__family=[family])
    return ret_user


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_client(user: User, client: APIClient) -> APIClient:
    client.force_authenticate(user)
    return client
