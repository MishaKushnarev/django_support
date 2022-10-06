from rest_framework.permissions import BasePermission

from apps.authentication.models import DEFAULT_ROLES


class OperatorOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.user.role.id == DEFAULT_ROLES["admin"]:
            return True
        return False


class ClientOnly(BasePermission):
    def has_permission(self, request, view=None) -> bool:
        if request.user.role.id == DEFAULT_ROLES["user"]:
            return True

        return False
