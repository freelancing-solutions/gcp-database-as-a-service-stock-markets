from data_service.store.stocks import Broker
from data_service.utils.utils import create_id
from pytest import raises
broker_instance: Broker = Broker()
# TODO add mocks for ndb calls

def assign_broker(this_broker_instance: Broker) -> Broker:
    this_broker_instance.broker_id = "1234567ydsdfsd"
    this_broker_instance.broker_name = "ABC"
    this_broker_instance.broker_code = "BCA"
    return this_broker_instance


def test_broker_instance():
    assert isinstance(broker_instance, Broker), "broker instance could not be instantiated"

def test_broker_id():
    b_id = create_id()
    assert broker_instance.broker_id is None, "broker instance broker_id starting out with its default value"
    broker_instance.broker_id = b_id
    assert broker_instance.broker_id == b_id, "broker_id could not be set correctly"
    with raises(TypeError):
        broker_instance.broker_id = 0
    with raises(ValueError):
        broker_instance.broker_id = ""

def test_broker_code():
    b_code = create_id()
    assert broker_instance.broker_code is None, "broker instance broker_code starting with a wrong default"
    broker_instance.broker_code = b_code
    assert broker_instance.broker_code == b_code, "broker instance broker_code could not be set correctly"
    with raises(TypeError):
        broker_instance.broker_code = -9
    with raises(ValueError):
        broker_instance.broker_code = ""

def test_broker_name():
    b_name = "ABcD"
    assert broker_instance.broker_name is None, "broker instance broker name starting with bad value"
    broker_instance.broker_name = b_name
    assert broker_instance.broker_name == b_name.lower(), "broker instance broker name could not be set correctly"

def test_broker_dunder_functions():
    first_broker: Broker = assign_broker(broker_instance)
    second_broker: Broker = assign_broker(broker_instance)
    assert first_broker == second_broker, "Equal does not pass"
    assert str(first_broker) == str(second_broker), "Str rep does not work"
