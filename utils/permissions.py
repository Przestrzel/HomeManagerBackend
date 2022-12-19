from abc import ABC

from rest_framework.permissions import BasePermission
from rest_framework.serializers import Serializer, IntegerField, ValidationError

from users.models import Family, User


class FamilyRequiredSerializer(Serializer):
    family = IntegerField(required=True)

    def create(self, validated_data):
        return None

    def update(self, instance, validated_data):
        return instance


class IsFamilyMember(BasePermission):
    message = "You are not a member of this family."

    def has_permission(self, request, view):
        try:
            request_serializer = FamilyRequiredSerializer(data=request.data)
            request_serializer.is_valid(raise_exception=True)
        except ValidationError:
            return False
        family = request_serializer.validated_data["family"]
        return User.objects.get(id=request.user.id).family.filter(id=family).exists()

    def has_object_permission(self, request, view, obj):
        self.message = "You have to provide a family id."
        return User.objects.get(id=request.user.id).family.filter(id=obj.family).exists()
