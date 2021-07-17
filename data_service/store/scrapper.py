from google.cloud import ndb


class Setters:
    def __init__(self):
        pass

    @staticmethod
    def set_id(prop, data_id: str) -> str:
        data_id = data_id.strip()
        if data_id is None or data_id == "":
            raise ValueError("{} is invalid".format(str(prop)))
        if not isinstance(data_id, str):
            raise TypeError("{} Invalid Type".format(str(prop)))
        return data_id

    @staticmethod
    def set_data(prop, data: str) -> str:
        if data is None or data == "":
            raise ValueError("{} is invalid".format(str(prop)))
        if not isinstance(data, str):
            raise TypeError("{} invalid Type".format(str(prop)))
        return data

    @staticmethod
    def set_status(prop, status: bool) -> bool:
        if not isinstance(status, bool):
            raise TypeError("{} invalid Type".format(str(prop)))
        return status


setters: Setters = Setters()


class ScrapperTempStore(ndb.Model):
    """
        used to store scrapped data from selenium
        this is data still waiting to be parsed
        the parser should to be able to fill in info from external api endpoints
        available
    """
    data_id = ndb.StringProperty(indexed=True, validator=setters.set_id)
    data = ndb.PickleProperty(validator=setters.set_data)
    status = ndb.BooleanProperty(default=True, validator=setters.set_status)

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.data_id != other.data_id:
            return False
        if self.status != other.status:
            return False
        return True

    def __str__(self) -> str:
        return "Status: {} Data: {}".format(str(self.status), str(self.data))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.data_id)

    def __bool__(self) -> bool:
        return bool(self.data_id)

