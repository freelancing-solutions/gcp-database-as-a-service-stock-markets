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

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']

        response, status = membership_view_instance.add_membership(uid=uid, plan_id=plan_id,
                                                                   plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert status == 500, response_data['message']

        mocker.patch('data_service.store.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('data_service.store.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('data_service.store.memberships.MembershipValidators.start_date_valid', return_value=True)
        # mocker.patch('data_service.views.memberships.Validators.can_add_member', return_value=True)

        response, status = membership_view_instance.add_membership(uid=uid, plan_id=plan_id,
                                                                   plan_start_date=plan_start_date)
        response_data: dict = response.get_json()
        assert status == 200, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_update_membership(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        plan_id = membership_mock_data['plan_id']
        plan_start_date = membership_mock_data['plan_start_date']
        mocker.patch('data_service.store.users.UserValidators.is_user_valid', return_value=True)
        mocker.patch('data_service.store.memberships.PlanValidators.plan_exist', return_value=False)
        mocker.patch('data_service.store.memberships.MembershipValidators.start_date_valid', return_value=True)
        response, status = membership_view_instance.update_membership(uid=uid, plan_id=plan_id,
                                                                      plan_start_date=plan_start_date)
        assert status == 200, "Unable to update membership"
        response_data: dict = response.get_json()
        assert response_data.get('message') is not None, "message was not set properly"
        assert response_data.get('payload') is not None, response_data['message']

    mocker.stopall()


# noinspection PyShadowingNames
def test_set_membership_status(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid = membership_mock_data['uid']
        status = membership_mock_data['status']
        response, status = membership_view_instance.set_membership_status(uid=uid, status=status)
        assert status == 200, "Unable to set membership status"
        response, status = membership_view_instance.set_membership_status(uid=uid, status="paid")
        assert status == 200, "Unable to set membership status"
    mocker.stopall()


# noinspection PyShadowingNames
def test_change_membership(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    membership_query_mock_instance = MembershipsQueryMock()
    membership_query_mock_instance.membership_instance.plan_id = membership_mock_data['plan_id']
    mocker.patch('google.cloud.ndb.Model.query', return_value=membership_query_mock_instance)
    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid: str = membership_mock_data['uid']
        plan_id: str = membership_mock_data['plan_id']
        dest_plan_id: str = create_id()
        mocker.patch('data_service.views.memberships.MembershipsView.plan_exist', return_value=True)
        response, status = membership_view_instance.change_membership(uid=uid, origin_plan_id=plan_id,
                                                                      dest_plan_id=dest_plan_id)
        assert status == 200, "Unable to change membership"

    mocker.stopall()


# noinspection PyShadowingNames
def test_send_welcome_email(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid: str = membership_mock_data['uid']
        plan_id: str = membership_mock_data['plan_id']
        response, status = membership_view_instance.send_welcome_email(uid=uid, plan_id=plan_id)
        assert status == 200, "unable to send welcome email"

    mocker.stopall()


# noinspection PyShadowingNames
def test_plan_members_payment_status(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        membership_view_instance: MembershipsView = MembershipsView()
        uid: str = membership_mock_data['uid']
        plan_id: str = membership_mock_data['plan_id']
        status: str = membership_mock_data['status']
        response, status = membership_view_instance.return_plan_members_by_payment_status(plan_id=plan_id, status=status)
        assert status == 200, "unable to fetch plan members by status"


    mocker.stopall()


# noinspection PyShadowingNames
def test_return_plan_members(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        pass

    mocker.stopall()

# noinspection PyShadowingNames
def test_is_member_off(mocker):
    mocker.patch('google.cloud.ndb.Model.put', return_value=create_id())
    mocker.patch('google.cloud.ndb.Model.query', return_value=MembershipsQueryMock())

    with test_app().app_context():
        pass

    mocker.stopall()

# noinspection PyShadowingNames
def test_payment_amount(mocker):
    pass

# noinspection PyShadowingNames
def test_set_payment_status(mocker):
    pass
