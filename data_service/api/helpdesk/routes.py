import typing
from flask import Blueprint, request, jsonify
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


@helpdesk_bp.route('api/v1/help-desk/ticket', methods=["POST", "GET"])
def get_support_ticket() -> tuple:
    request_data: dict = request.get_json()
    if ("ticket_id" in request_data) and (request_data["ticket_id"] != ""):
        ticket_id: typing.Union[str, None] = request_data.get('ticket_id')
    else:
        return jsonify({'status': False, 'message': 'ticket_id is required'}), 500

    ticket_view_instance: TicketView = TicketView()
    return ticket_view_instance.fetch_ticket(ticket_id=ticket_id)
