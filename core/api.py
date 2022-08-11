from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
    operator = UserSerializer()
    client = UserSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


class TicketLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "theme", "resolved", "operator", "client"]


@api_view(["GET"])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    data = TicketSerializer(tickets, many=True).data
    return Response(data=data)


@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    return Response(data=data)
