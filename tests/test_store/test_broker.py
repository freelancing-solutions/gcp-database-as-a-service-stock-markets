from data_service.store.stocks import Broker
from data_service.utils.utils import create_id

broker_instance: Broker = Broker()
# TODO add mocks for ndb calls
def test_broker_instance():
    assert isinstance(broker_instance, Broker), "broker instance could not be instantiated"

def test_broker_id():
    b_id = create_id()
    assert broker_instance.broker_id is None, "broker instance broker_id starting out with its default value"
    broker_instance.broker_id = b_id
    assert broker_instance.broker_id == b_id, "broker_id could not be set correctly"

def test_broker_code():
    b_code = create_id()
    assert broker_instance.broker_code is None, "broker instance broker_code starting with a wrong default"
    broker_instance.broker_code = b_code
    assert broker_instance.broker_code == b_code, "broker instance broker_code could not be set correctly"

def test_broker_name():
    b_name = "ABcD"
    assert broker_instance.broker_name is None, "broker instance broker name starting with bad value"
    broker_instance.broker_name = b_name
    assert broker_instance.broker_name == b_name.lower(), "broker instance broker name could not be set correctly"



