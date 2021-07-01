import typing
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from data_service.api.api_authenticator import handle_auth
from data_service.config.exceptions import InputError
from data_service.utils.utils import date_string_to_date
from data_service.views.helpdesk import TicketView

helpdesk_bp = Blueprint('helpdesk', __name__)


@helpdesk_bp.route('/api/v1/helpdesk-messages', methods=["GET", "POST"])
def helpdesk_messages() -> tuple:
    pass


@helpdesk_bp.route('/api/v1/helpdesk-tickets', methods=["GET", "POST"])
def helpdesk_tickets() -> tuple:
    ticket_view_instance: TicketView = TicketView()
    return ticket_view_instance.get_all_tickets()


@helpdesk_bp.route('/api/v1/helpdesk-unresolved', methods=["POST", "GET"])
def unresolved_tickets() -> tuple:
    ticket_view_instance: TicketView = TicketView()
    return ticket_view_instance.get_unresolved_tickets()


@helpdesk_bp.route('/api/v1/helpdesk-resolved', methods=["POST", "GET"])
def resolved_tickets() -> tuple:
    ticket_view_instance: TicketView = TicketView()
    return ticket_view_instance.get_resolved_tickets()
