from django.urls import path

from core.api import TicketAssignAPI, TicketRetrieveAPI, TicketsCreateListAPI

urlpatterns = [
    path("", TicketsCreateListAPI.as_view()),
    path("<int:id>/", TicketRetrieveAPI.as_view()),
    path("<int:id>/assign/", TicketAssignAPI.as_view()),
]
