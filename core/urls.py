from django.urls import path

from core.api import get_all_tickets

urlpatterns = [
    path("", get_all_tickets),
]
