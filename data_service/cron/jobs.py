# Cron jobs for stock trading app
from data_service.views.memberships import MembershipsView


def cron_pay_memberships():
    """
        cron job 400 860
        function: executes payments for memberships depending on the payment plans
    """
    memberships_view: MembershipsView = MembershipsView()


def cron_down_grade_unpaid_memberships():
    """
        cron job
        function: when executed go over all membership plans and downgrade those members who are not paid
    """
    pass


def cron_send_affiliate_payments():
    """
        cron job
        function: when executed go over all affiliate records and gather payment data and send to recruiter wallet
    """
    pass


def cron_send_login_reminders():
    pass


def cron_send_payment_reminders():
    pass


def cron_send_affiliate_notifications():
    pass


# stock related cron jobs
def cron_access_external_stock_api():
    pass


def cron_perform_net_calculations():
    pass


