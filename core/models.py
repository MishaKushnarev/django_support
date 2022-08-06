from django.conf import settings
from django.db import models

from shared.django.models import TimeStampMixin


class Ticket(TimeStampMixin):
    theme = models.CharField(max_length=255)
    description = models.TextField()
    resolved = models.BooleanField(default=False)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_tickets",
    )
    operator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="operator_tickets",
    )

    def __str__(self) -> str:
        return f"{self.operator} | {self.theme}"


class Comment(TimeStampMixin):
    text = models.TextField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="comments",
    )
    ticket = models.ForeignKey(
        "Ticket",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    prev_comment = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="next",
    )

    def __str__(self) -> str:
        return str(self.ticket)
