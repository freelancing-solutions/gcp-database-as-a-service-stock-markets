from data_service.cron.utils.utils import send_email
from data_service.views.users import UserView
import asyncio
from data_service.config import Config


def cron_send_login_reminders():
    """
        from users fetch those who haven't logged in for a while
        take their email address and send them a login reminder
    """
    coro: list = []
    body: str = """
        This is to remind you to login into your account
        in order for you to login 
        <strong> please click the link below</strong> 
    """
    config_instance: Config = Config()
    subject: str = "Reminder to login at : {}".format(config_instance.APP_NAME)

    user_view_instance: UserView = UserView()
    response, status = user_view_instance.get_in_active_users()
    response_data: dict = response.get_json()
    if response_data['status']:
        users_list = response_data['payload']
        for user in users_list:
            coro.append(send_email(to=user['email'], subject=subject, body=body))

    loop = asyncio.new_event_loop()
    loop.run_until_complete(asyncio.wait(coro))
    return 'OK', 200


def cron_send_payment_reminders():
    pass


def cron_send_affiliate_notifications():
    """
        for each affiliate compile a report including the following
            total recruited so far
            total recruited this month
            total amount earned so far
            total amount earned this month
            last recruitment date
            recruits list
    """
    pass


def cron_perform_net_calculations():
    pass


