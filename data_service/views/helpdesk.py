import typing
from flask import jsonify
from data_service.store.helpdesk import HelpDeskValid, TicketValid, TicketThreadValid, Ticket
from data_service.store.helpdesk import HelpDesk
from data_service.utils.utils import create_id
from data_service.config.exception_handlers import handle_view_errors
from data_service.config.use_context import use_context
import re
import functools


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
    async def is_user_async(uid: str) -> bool:
        return True

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """
            TODO - check if user owns email
            TODO - or if email is being used by another user
        """
        regex = '\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'
        return True if re.search(regex, email) is not None else False

    @staticmethod
    def is_cell_valid(cell: str) -> bool:
        """
            TODO - check if user owns cell
            TODO - or if cell is being used by another user
        """
        pass

    @staticmethod
    async def is_cell_valid_async(cell: str) -> bool:
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


# noinspection DuplicatedCode
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
        if key is None:
            return jsonify({'status': False, 'message': 'Error updating database'}), 500
        return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                        'message': 'help desk created'}), 200

    @use_context
    @handle_view_errors
    async def create_help_desk_async(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'help desk already created'}), 200
        help_desk_instance = HelpDesk()
        key = help_desk_instance.put()
        if key is None:
            return jsonify({'status': False, 'message': 'Error updating database'}), 500
        return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                        'message': 'help desk created'}), 200

    @use_context
    @handle_view_errors
    @functools.lru_cache(maxsize=1)
    def get_help_desk(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'successfully fetched helpdesk'}), 200

        return jsonify({'status': False, 'message': 'unable to find helpdesk'}), 500

    @use_context
    @handle_view_errors
    @functools.lru_cache(maxsize=1)
    async def get_help_desk_async(self) -> tuple:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
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
    async def add_ticket_async(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
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

    @use_context
    async def close_ticket_async(self) -> bool:
        help_desk_instance: HelpDesk = HelpDesk.query().get_async().get_result()
        if isinstance(help_desk_instance, HelpDesk):
            help_desk_instance.total_tickets_opened -= 1
            help_desk_instance.total_tickets_closed += 1
            help_desk_instance.put_async().get_result()
            return True
        return False


# noinspection DuplicatedCode
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

            if key is None:
                return jsonify({'status': False, 'message': 'Error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully created ticket'}), 200

    @use_context
    @handle_view_errors
    async def create_ticket_async(self, uid: str, topic: str, subject: str, message: str,
                                  email: str,  cell: str) -> tuple:
        if self.is_ticket_valid(uid=uid, topic=topic, subject=subject, message=message,
                                email=email, cell=cell):
            ticket_instance: Ticket = Ticket()
            ticket_instance.ticket_id = create_id()
            ticket_instance.uid = uid
            ticket_instance.topic = topic
            ticket_instance.subject = subject
            ticket_instance.message = message
            ticket_instance.email = email
            ticket_instance.cell = cell
            key = ticket_instance.put_async().get_result()

            if key is None:
                return jsonify({'status': False, 'message': 'Error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully created ticket'}), 200

    @use_context
    @handle_view_errors
    def resolve_ticket(self, ticket_id: str) -> tuple:
        """
            ticket_id: str
            return: resolved ticket
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.is_resolved = True

            key = ticket_instance.put()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully resolved ticket'}), 200

        return jsonify({'status': False, 'message': 'Ticket not found'}), 500

    @use_context
    @handle_view_errors
    async def resolve_ticket_async(self, ticket_id: str) -> tuple:
        """
            ticket_id: str
            return: resolved ticket
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.is_resolved = True
            key = ticket_instance.put_async().get_result()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully resolved ticket'}), 200

        return jsonify({'status': False, 'message': 'Ticket not found'}), 500

    @use_context
    @handle_view_errors
    def update_ticket(self, ticket_id: typing.Union[str, None], topic: typing.Union[str, None] = None,
                      subject: typing.Union[str, None] = None, message: typing.Union[str, None] = None,
                      email: str = typing.Union[str, None], cell: typing.Union[str, None] = None,
                      assigned_to_uid: typing.Union[str, None] = None) -> tuple:

        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            if topic is not None:
                ticket_instance.topic = topic
            if subject is not None:
                ticket_instance.subject = subject
            if message is not None:
                ticket_instance.message = message
            if email is not None:
                ticket_instance.email = email
            if cell is not None:
                ticket_instance.cell = cell
            if assigned_to_uid is not None:
                ticket_instance.assigned_to_uid = assigned_to_uid
            key = ticket_instance.put()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    async def update_ticket_async(self, ticket_id: typing.Union[str, None], topic: typing.Union[str, None] = None,
                                  subject: typing.Union[str, None] = None, message: typing.Union[str, None] = None,
                                  email: str = typing.Union[str, None], cell: typing.Union[str, None] = None,
                                  assigned_to_uid: typing.Union[str, None] = None) -> tuple:

        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            if topic is not None:
                ticket_instance.topic = topic
            if subject is not None:
                ticket_instance.subject = subject
            if message is not None:
                ticket_instance.message = message
            if email is not None:
                ticket_instance.email = email
            if cell is not None:
                ticket_instance.cell = cell
            if assigned_to_uid is not None:
                ticket_instance.assigned_to_uid = assigned_to_uid
            key = ticket_instance.put_async().get_result()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    def assign_ticket(self, ticket_id: str, assigned_to_uid: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.assigned_to_uid = assigned_to_uid
            key = ticket_instance.put()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    async def assign_ticket_async(self, ticket_id: str, assigned_to_uid: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.assigned_to_uid = assigned_to_uid
            key = ticket_instance.put_async().get_result()
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    def send_response_by_email(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send email response mark ticket save ticket save response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    async def send_response_by_email_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send email response mark ticket save ticket save response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put_async().get_result()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    def send_sms_notification(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send notification update ticket to reflect that notification was sent
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    async def send_sms_notification_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket send notification update ticket to reflect that notification was sent
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put_async().get_result()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    def add_response(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket add response
        """
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    async def add_response_async(self, ticket_id: str, subject: str, message: str) -> tuple:
        """
            find ticket add response
        """
        ticket_instance: Ticket = Ticket.query(
            Ticket.ticket_id == ticket_id).get_async().get_result()
        if isinstance(ticket_instance, Ticket):
            ticket_instance.response_sent = True
            key = ticket_instance.put_async().get_result()
            # TODO Send response here
            if key is None:
                return jsonify({'status': False, 'message': 'General error updating database'}), 500
            return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                            'message': 'successfully updated ticket'}), 200
        return jsonify({'status': False, 'message': 'Unable to find ticket'}), 500

    @use_context
    @handle_view_errors
    def get_all_tickets(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query().fetch()]
        return jsonify({'status': True, 'payload': tickets_list, 'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    async def get_all_tickets_async(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query().fetch_async().get_result()]
        return jsonify({'status': True, 'payload': tickets_list, 'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    def get_unresolved_tickets(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == False).fetch()]
        return jsonify({'status': True, 'payload': tickets_list,
                        'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    async def get_unresolved_tickets_async(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == False).fetch_async().get_result()]
        return jsonify({'status': True, 'payload': tickets_list,
                        'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    def get_resolved_tickets(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == True).fetch()]
        return jsonify({'status': True, 'payload': tickets_list,
                        'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    async def get_resolved_tickets_async(self) -> tuple:
        tickets_list: typing.List[dict] = [ticket.to_dict() for ticket in Ticket.query(
            Ticket.is_resolved == True).fetch_async().get_result()]
        return jsonify({'status': True, 'payload': tickets_list,
                        'message': 'successfully returned tickets'}), 200

    @use_context
    @handle_view_errors
    def fetch_ticket(self, ticket_id: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get()
        return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                        'message': 'successfully returned ticket'}), 200

    @use_context
    @handle_view_errors
    async def fetch_ticket_async(self, ticket_id: str) -> tuple:
        ticket_instance: Ticket = Ticket.query(Ticket.ticket_id == ticket_id).get_async().get_result()
        return jsonify({'status': True, 'payload': ticket_instance.to_dict(),
                        'message': 'successfully returned ticket'}), 200


class TicketThreadView(Validators):
    pass
