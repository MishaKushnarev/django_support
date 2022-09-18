from django.core.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import DEFAULT_ROLES
from core.models import Ticket
from core.permissons import ClientOnly, OperatorOnly
from core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
)


class TicketsCreateListAPI(ListAPIView, CreateAPIView):
    """If method GET - return all tickets
    If method POST - create ticket"""

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer
    permission = ClientOnly

    def get_queryset(self):
        link_parameter = self.request.query_params["empty"]
        user = self.request.user

        if user.role.id == DEFAULT_ROLES["admin"]:

            if link_parameter == "true":
                return Ticket.objects.filter(operator=None)
            elif link_parameter == "false":
                return Ticket.objects.filter(Q(operator=None) | Q(operator=user))
            raise ValidationError

        if user.role.id != DEFAULT_ROLES["admin"]:
            raise ValueError("Permission denied")

        elif link_parameter == "true":
            pass
        elif link_parameter == "false":
            pass
        else:
            raise ValueError("Bad format empty")

    def post(self, request):
        if self.permission.has_permission(self, request=request):
            serializer = TicketSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise PermissionDenied

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TicketLightSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketRetrieveAPI(RetrieveAPIView):
    """Get one ticket with full information"""

    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"

    def get_queryset(self):
        user = self.request.user
        if user.role.id == DEFAULT_ROLES["user"]:
            return Ticket.objects.filter(client=user)
        return Ticket.objects.filter(operator=user)


class TicketAssignAPI(UpdateAPIView):
    """Assign ticket with operator"""

    http_method_names = ["patch"]
    serializer_class = TicketAssignSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"
    permission_classes = [OperatorOnly]

    def get_queryset(self):
        return Ticket.objects.filter(operator=None)


# @permission_classes([IsAuthenticatedOrReadOnly])
# @api_view(["GET", "POST"])
# def get_post_tickets(request):
#     if request.method == "GET":
#         tickets = Ticket.objects.all()
#         data = TicketLightSerializer(tickets, many=True).data
#         return Response(data=data)

#     serializer = TicketSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     instance: Ticket = serializer.create(serializer.validated_data)
#     results: dict = TicketSerializer(instance).data

#     return Response(data=results, status=status.HTTP_201_CREATED)


# @permission_classes([IsAuthenticated])
# @api_view(["GET", "PUT", "DELETE"])
# def get_ticket(request, id_: int):

#     ticket = Ticket.objects.get(id=id_)
#     if request.method == "GET":
#         data = TicketSerializer(ticket).data
#         return Response(data=data)

#     elif request.method == "PUT":
#         serializer = TicketSerializer(instance=ticket, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             instance = serializer.update(instance=ticket, validated_data=serializer.validated_data)
#             result = TicketSerializer(instance).data
#             return Response(result, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == "DELETE":
#         ticket.delete()
#         message_ = {"message": "Ticket - delete"}
#         return Response(message_, status=status.HTTP_204_NO_CONTENT)
