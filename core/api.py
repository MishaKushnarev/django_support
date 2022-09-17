# from django.db.models import Q
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from authentication.models import DEFAULT_ROLES
from core.models import Ticket
from core.permissons import OperatorOnly
from core.serializers import (
    TicketAssignSerializer,
    TicketLightSerializer,
    TicketSerializer,
)

# class TicketsCreateAPI(CreateAPIView):
#     serializer_class = TicketSerializer
#     queryset = Ticket.objects.all()


# class TicketsListAPI(ListAPIView):
#     serializer_class = TicketLightSerializer

#     def get_queryset(self):
#         user = self.request.user

#         if user.role.id == DEFAULT_ROLES["admin"]:
#             return Ticket.objects.filter(client=user)

#         return Ticket.objects.filter(Q(operator=None) | Q(operator=user))


class TicketsCreateListAPI(ListAPIView, CreateAPIView):
    """If method GET - return all tickets
    If method POST - create ticket"""

    permission_classes = [IsAuthenticated]
    serializer_class = TicketLightSerializer

    def get_queryset(self):
        return Ticket.objects.all()

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
