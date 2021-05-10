import typing
from datetime import datetime
from random import randint

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

    def __init__(self):
        pass

    def fetch(self):
        pass

    def get(self):
        pass


def test_create_membership():
    pass

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

