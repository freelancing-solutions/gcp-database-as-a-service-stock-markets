
from data_service.utils.utils import task_counter


def test_timer():
    z = 0
    for i in task_counter():
        assert z == i, "task counter generator not working"
        z += 1




