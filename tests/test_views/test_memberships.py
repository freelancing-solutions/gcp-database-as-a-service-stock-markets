import typing
from datetime import datetime, timedelta
from random import randint

from google.cloud import ndb

from data_service.views.memberships import MembershipsView
from data_service.store.memberships import Memberships
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class MembershipsQueryMock:
    membership_instance: Memberships = Memberships()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Memberships]:
        return [self.membership_instance for _ in range(self.results_range)]

    def get(self) -> Memberships:
        return self.membership_instance

    @ndb.tasklet
    def get_async(self):
        return self.membership_instance


membership_mock_data: dict = {
    "uid": create_id(),
    "plan_id": create_id(),
    "status": "unpaid",
    "date_created": datetime.now(),
    "plan_start_date": datetime.date(datetime.now() + timedelta(days=5))
}


# noinspection PyShadowingNames
def test_create_membership(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    # noinspection PyShadowingNames
    def validator_mocker(mocker):
        yield True

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        plan_id = membership_mock_data['plan_id']
        status = membership_mock_data['status']
        date_created = membership_mock_data['date_created']
        plan_start_date = membership_mock_data['plan_start_date']

        response, status = membership_view_instance.add_membership(uid=uid, plan_id=plan_id,
                                                                   plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert status == 500, response_data['message']

        mocker.patch('data_service.store.users.UserValidators.is_user_valid', return_value=validator_mocker)
        mocker.patch('data_service.store.memberships.PlanValidators.plan_exist', return_value=not validator_mocker)
        mocker.patch('data_service.store.memberships.MembershipValidators.start_date_valid',
                     return_value=validator_mocker)

        response, status = membership_view_instance.add_membership(uid=uid, plan_id=plan_id,
                                                                   plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']

    mocker.stopall()


def test_update_membership():
    pass


def test_set_membership_status():
    pass


def test_change_membership():
    pass


def test_send_welcome_email():
    pass


def test_plan_members_payment_status():
    pass


def test_return_plan_members():
    pass


def test_is_member_off():
    pass


def test_payment_amount():
    pass


def test_set_payment_status():
    pass
