from abc import ABC

from dj_rest_auth.serializers import (
    UserDetailsSerializer as RestAuthUserDetailsSerializer,
    LoginSerializer as RestAuthLoginSerializer
)
from rest_framework import serializers

from users.models import Person, Family


class FamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = Family
        fields = ('family_name',)


class PersonSerializer(serializers.ModelSerializer):
    family = FamilySerializer(read_only=True, many=True)

    class Meta:
        model = Person
        fields = ('first_name', 'last_name', 'date_of_birth', 'family')


class UserDetailsSerializer(RestAuthUserDetailsSerializer):
    person = PersonSerializer(read_only=True)

    class Meta(RestAuthUserDetailsSerializer.Meta):
        fields = RestAuthUserDetailsSerializer.Meta.fields + ("email", "person")
        read_only_fields = ("email",)


class LoginSerializer(RestAuthLoginSerializer):
    username = None
    email = serializers.EmailField(required=True)
