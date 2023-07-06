from abc import ABC
import json
from rest_framework.permissions import BasePermission
from rest_framework.serializers import ValidationError

from users.models import User
from utils.serializers import FamilyRequiredSerializer


class IsFamilyMember(BasePermission):
    message = "You are not a member of this family"

    def has_permission(self, request, view):
        try:
            family_id = request.COOKIES.get("X-Family-Id")
            request_serializer = FamilyRequiredSerializer(data={"family": family_id})
            request_serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.message = "Family id must be provided by X-Family-Id"
            return False
        family = request_serializer.validated_data["family"]
        return User.objects.get(id=request.user.id).family.filter(id=family).exists()

    def has_object_permission(self, request, view, obj):
        self.message = "You have to provide a family id"
        return User.objects.get(id=request.user.id).family.filter(id=obj.family).exists()
