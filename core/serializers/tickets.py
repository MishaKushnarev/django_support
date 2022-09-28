from itertools import chain

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from authentication.models import Role
from core.models import Ticket

User = get_user_model()


def user_as_dict(user: User) -> dict:
    return {
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "first_name": user.phone,
        "last_name": user.phone,
        "age": user.phone,
    }


def ticket_as_dict(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,  # type: ignore
        "theme": ticket.theme,
        "description": ticket.description,
        "operator": user_as_dict(ticket.operator),
        "resolved": ticket.resolved,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
    }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        exclude = [
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        exclude = [
            "password",
            "last_login",
            "updated_at",
            "is_active",
            "is_staff",
            "is_superuser",
            "created_at",
            "updateed_at",
            "groups",
            "user_permissions",
        ]


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"

    def validate(self, attrs: dict) -> dict:

        theme = attrs.get("theme")

        if not theme:
            return attrs

        data = Ticket.objects.values_list("theme")

        for element in chain.from_iterable(data):
            if element == theme:
                raise ValidationError("This ticket is already in database")

        attrs["client"] = self.context["request"].user

        return attrs


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "theme", "resolved", "operator", "client"]


class TicketAssignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["operator"]

    def validate(self, attrs: dict) -> dict:
        attrs["operator"] = self.context["request"].user
        return attrs
