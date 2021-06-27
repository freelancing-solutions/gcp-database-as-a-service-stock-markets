import functools
import typing
from google.api_core.exceptions import RetryError, Aborted
from flask import jsonify, current_app
from datetime import datetime, date
from data_service.store.helpdesk import HelpDeskValid, TicketValid, TicketThreadValid, Ticket
from data_service.store.helpdesk import HelpDesk
from data_service.utils.utils import create_id
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


class Validators(HelpDeskValid, TicketValid, TicketThreadValid):
    """
        helpdesk input validators
    """

    def __init__(self):
        super(Validators, self).__init__()

    @staticmethod
    def is_user(uid: str) -> bool:
        """
            TODO find out if uid contains valid user
        """
        return True

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
            TODO - check if user owns email
            TODO - or if email is being used by another user
        """
        return True

    @staticmethod
    def is_cell_valid(cell: str) -> bool:
        """
            TODO - check if user owns cell
            TODO - or if cell is being used by another user
        """
        pass

    def is_ticket_valid(self, uid: str, topic: str, subject: str, message: str, email: str, cell: str) -> bool:
        """
            TODO- validate ticket
        """
        valid_user: bool = self.is_user(uid=uid)
        valid_topic: bool = self.is_topic_valid(topic=topic)
        valid_subject: bool = self.is_subject_valid(subject=subject)
        valid_message: bool = self.is_message_valid(message=message)
        valid_email: bool = self.is_email_valid(email=email)
        valid_cell: bool = self.is_cell_valid(cell=cell)
        return valid_user and valid_topic and valid_subject and valid_message and valid_email and valid_cell


class HelpDeskView(Validators):

    def __init__(self):
        super(HelpDeskView, self).__init__()

    @use_context
    @handle_view_errors
    def create_help_desk(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'help desk already created'}), 200
        help_desk_instance = HelpDesk()
        key = help_desk_instance.put()
        return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                        'message': 'help desk created'}), 200

    @use_context
    @handle_view_errors
    def get_help_desk(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'successfully fetched helpdesk'}), 200

        return jsonify({'status': False, 'message': 'unable to find helpdesk'}), 500

    @use_context
    def add_ticket(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            help_desk_instance.total_tickets += 1
            help_desk_instance.total_tickets_opened += 1
            help_desk_instance.put()
            return True
        return False

    @use_context
    def close_ticket(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            help_desk_instance.total_tickets_opened -= 1
            help_desk_instance.total_tickets_closed += 1
            help_desk_instance.put()
            return True
        return False


class TicketView(Validators):
    def __init__(self):
        super(TicketView, self).__init__()

    @use_context
    @handle_view_errors
    def create_ticket(self, uid: str, topic: str, subject: str, message: str, email: str,
                      cell: str) -> tuple:
        if self.is_ticket_valid(uid=uid, topic=topic, subject=subject, message=message, email=email,
                                cell=cell):
            ticket_instance: Ticket = Ticket()
            ticket_instance.ticket_id = create_id()
            ticket_instance.uid = uid
            ticket_instance.topic = topic
            ticket_instance.subject = subject
            ticket_instance.message = message
            ticket_instance.email = email
            ticket_instance.cell = cell
            key = ticket_instance.put()
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully created ticket'}), 200

    def close_ticket(self):
        pass

    def update_ticket(self):
        pass

    def assign_ticket(self):
        pass

    def send_response_by_email(self):
        pass

    def send_sms_notification(self):
        pass

    def resolve_ticket(self):
        pass

    def add_response(self):
        pass


class TicketThreadView(Validators):
    pass
