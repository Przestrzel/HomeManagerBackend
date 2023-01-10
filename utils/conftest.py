import pytest
from rest_framework.test import APIClient

from users.models import User
from users.tests.factories import UserFactory


@pytest.fixture
def user() -> User:
    ret_user: User = UserFactory.create()
    return ret_user


@pytest.fixture
def client() -> APIClient:
    return APIClient()


@pytest.fixture
def user_client(user: User, client: APIClient) -> APIClient:
    client.force_authenticate(user)
    return client
