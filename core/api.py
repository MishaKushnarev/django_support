from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Ticket
from core.serializers import TicketLightSerializer, TicketSerializer


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


@api_view(["GET"])
def get_ticket(request, id_: int):
    tickets = Ticket.objects.get(id=id_)
    data = TicketSerializer(tickets).data
    return Response(data=data)
