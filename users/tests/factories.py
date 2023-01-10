import datetime
from django.conf import settings
import factory
from factory.django import DjangoModelFactory
from factory import Faker, SubFactory, fuzzy
import datetime

from users.models import Family, User, Person


class FamilyFactory(DjangoModelFactory):
    family_name = Faker("name")

    class Meta:
        model = Family


class PersonFactory(DjangoModelFactory):
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    date_of_birth = fuzzy.FuzzyDate(
        datetime.date(2020, 1, 1),
        datetime.date(2023, 12, 31),
    )

    class Meta:
        model = Person

    @factory.post_generation
    def family(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for family in extracted:
            print(extracted)
            self.family.add(family)


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    password = Faker("password")
    person = SubFactory(PersonFactory)

    class Meta:
        model = User
