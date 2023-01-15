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
            data = request.query_params if request.method == "GET" else request.data
            request_serializer = FamilyRequiredSerializer(data=data)
            request_serializer.is_valid(raise_exception=True)
        except ValidationError:
            self.message = "Family id must be provided"
            return False
        family = request_serializer.validated_data["family"]
        return User.objects.get(id=request.user.id).family.filter(id=family).exists()

    def has_object_permission(self, request, view, obj):
        self.message = "You have to provide a family id"
        return User.objects.get(id=request.user.id).family.filter(id=obj.family).exists()
