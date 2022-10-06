from apps.core.models import Ticket


class TicketsCRUD:
    @staticmethod
    def change_resolved_status(instance: Ticket) -> Ticket:
        """Change Ticke object's resolved status to the opposite"""
        instance.resolved = not instance.resolved
        instance.save()

        return instance
