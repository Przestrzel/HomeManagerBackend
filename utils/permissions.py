from rest_framework import permissions as rest_permissions


class IsFamilyMember(rest_permissions.BasePermission):
    message = "You are not a member of this family."

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        return obj.family.filter(members=request.user).exists()
