from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


class TicketsListAPI(ListAPIView):
    serializer_class = TicketLightSerializer
    queryset = Ticket.objects.all()


class TicketsCreateAPI(CreateAPIView):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    permission_classes = [IsAuthenticated]


class TicketRetrieveAPI(RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = "id"
    lookup_url_kwarg = "id"


@permission_classes([IsAuthenticatedOrReadOnly])
@api_view(["GET", "POST"])
def get_post_tickets(request):
    if request.method == "GET":
        tickets = Ticket.objects.all()
        data = TicketLightSerializer(tickets, many=True).data
        return Response(data=data)

    serializer = TicketSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    instance: Ticket = serializer.create(serializer.validated_data)
    results: dict = TicketSerializer(instance).data

    return Response(data=results, status=status.HTTP_201_CREATED)


@permission_classes([IsAuthenticated])
@api_view(["GET", "PUT", "DELETE"])
def get_ticket(request, id_: int):

    ticket = Ticket.objects.get(id=id_)
    if request.method == "GET":
        data = TicketSerializer(ticket).data
        return Response(data=data)

    elif request.method == "PUT":
        serializer = TicketSerializer(instance=ticket, data=request.data)
        if serializer.is_valid(raise_exception=True):
            instance = serializer.update(instance=ticket, validated_data=serializer.validated_data)
            result = TicketSerializer(instance).data
            return Response(result, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        ticket.delete()
        message_ = {"message": "Ticket - delete"}
        return Response(message_, status=status.HTTP_204_NO_CONTENT)
