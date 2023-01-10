from django.conf import settings
import pytest
from users.models import Family, User, Person
from users.tests.factories import UserFactory, FamilyFactory, PersonFactory


@pytest.mark.django_db
def test_create_family():
    family = FamilyFactory()
    Family.save(family)
    assert Family.objects.count() == 1


@pytest.mark.django_db
def test_create_user():
    family = FamilyFactory()
    user = UserFactory.create(person__family=[family])
    User.save(user)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_create_person():
    family = FamilyFactory()
    person = PersonFactory(family=[family])
    Person.save(person)
    assert Person.objects.count() == 1
