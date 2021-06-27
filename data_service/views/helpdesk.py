import functools
import typing
from google.api_core.exceptions import RetryError, Aborted
from flask import jsonify, current_app
from datetime import datetime, date
from data_service.store.helpdesk import HelpDeskValid, TicketValid, TicketThreadValid
from data_service.store.helpdesk import HelpDesk
from data_service.views.exception_handlers import handle_view_errors
from data_service.views.use_context import use_context


class Validators(HelpDeskValid, TicketValid, TicketThreadValid):
    """
        helpdesk input validators
    """
    pass


class HelpDeskView(Validators):

    def __init__(self):
        pass

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
    def get_help_desk(self):
        help_desk_instance: HelpDesk = HelpDesk.query().get()
        if isinstance(help_desk_instance, HelpDesk):
            return jsonify({'status': True, 'payload': help_desk_instance.to_dict(),
                            'message': 'successfully fetched helpdesk'}), 200

        return jsonify({'status': False, 'message': 'unable to find helpdesk'}), 500


class TicketView(Validators):
    pass


class TicketThreadView(Validators):
    pass
