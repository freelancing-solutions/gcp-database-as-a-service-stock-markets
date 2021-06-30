# Cron jobs for stock trading app
import datetime
import typing

from google.cloud import ndb

from data_service.store.wallet import WalletModel
from data_service.views.memberships import MembershipsView
from data_service.store.memberships import Memberships, MembershipPlans
from data_service.store.affiliates import Affiliates, Recruits, EarningsData
import asyncio


def return_plan_by_id(plan_id: str, payment_plans: typing.List[MembershipPlans]) -> typing.Union[MembershipPlans, None]:

    for plan in payment_plans:
        if plan.plan_id == plan_id:
            return plan
    return None


async def create_invoice(membership_plan, membership) -> bool:
    """
        create membership invoices here
    """
    pass


def cron_create_membership_invoices():
    """
        cron job 400 860
        function: executes payments for memberships depending on the payment plans
    """
    schedule_days = [1, 2, 3, 4, 5]
    today_date: datetime.date = datetime.datetime.now().date()
    memberships_list: typing.List[Memberships] = Memberships.query(Memberships.status == "unpaid").fetch()
    payment_plans_list: typing.List[MembershipPlans] = MembershipPlans.query().fetch()
    coro: list = []
    for membership in memberships_list:
        if membership.plan_start_date <= today_date:
            membership_plan = return_plan_by_id(plan_id=membership.plan_id, payment_plans=payment_plans_list)
            if membership_plan is not None:
                # Process Payment
                coro.append(create_invoice(membership_plan=membership_plan, membership=membership))
    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.wait(coro))


def cron_down_grade_unpaid_memberships():
    """
        cron job
        function: when executed go over all membership plans and downgrade those members who are not paid
    """
    pass


async def add_earnings(affiliate: Affiliates, earnings: EarningsData):
    # validate and refactor the below code
    wallet_instance: WalletModel = await WalletModel.query(WalletModel.uid == affiliate.uid).get_async()
    wallet_instance.available_funds = wallet_instance.available_funds + earnings.total_earned
    earnings.is_paid = True
    wallet_instance.put_async()
    earnings.put_async()


def cron_finalize_affiliate_payments():
    """
        cron job
        function: when executed go over all affiliate records and gather payment data
        and send to recruiter wallet
    """
    affiliates_list: typing.List[Affiliates] = Affiliates.query().fetch()
    coro: list = []
    for affiliate in affiliates_list:
        earnings_data: EarningsData = EarningsData.query(EarningsData.affiliate_id == affiliate.affiliate_id).get()
        if not earnings_data.is_paid:
            coro.append(add_earnings(affiliate=affiliate, earnings=earnings_data))

    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.wait(coro))


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


