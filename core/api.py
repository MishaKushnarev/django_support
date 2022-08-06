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
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "age": user.age,
    }


def ticket_as_dict(ticket: Ticket) -> dict:
    return {
        "id": ticket.id,
        "discriptions": ticket.discription,
        "theme": ticket.theme,
        "operator": user_as_dict(ticket.operator),
        "resolved": ticket.resolved,
        "created_at": ticket.created_at,
        "updated_at": ticket.updated_at,
    }


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    operator = UserSerializer()
    client = UserSerializer()

    class Meta:
        model = Ticket
        fields = "__all__"


@api_view(["GET"])
def get_all_tickets(request):
    tickets = Ticket.objects.all()
    data = TicketSerializer(tickets, many=True).data
    return Response(data=data)
