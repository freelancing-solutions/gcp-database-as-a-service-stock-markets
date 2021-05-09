import typing
from datetime import datetime
from random import randint

from data_service.views.affiliates import RecruitsView
from data_service.store.affiliates import Recruits
from data_service.utils.utils import create_id
from .. import test_app
# noinspection PyUnresolvedReferences
from pytest import raises
# noinspection PyUnresolvedReferences
from pytest_mock import mocker


class RecruitsQueryMock:
    recruits_instance: Recruits = Recruits()
    results_range: int = randint(0, 100)

    def __init__(self):
        pass

    def fetch(self) -> typing.List[Recruits]:
        return [self.recruits_instance for _ in range(self.results_range)]

    def get(self) -> Recruits:
        return self.recruits_instance



