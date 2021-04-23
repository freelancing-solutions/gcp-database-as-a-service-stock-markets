from google.cloud import ndb

class ScrapperTempStore(ndb.Model):
    """
        used to store scrapped data from sellenium
        this is data still waiting to be parsed
        the parser should to be able to fill in info from external api endpoints
        available
    """

    def set_id(self, data_id: str) -> str:
        data_id = data_id.strip()
        if data_id is None or data_id == "":
            raise ValueError("{} is invalid".format(self.name))

        if not isinstance(data_id, str):
            raise TypeError("{} Invalid Type".format(self.name))

        return data_id

    def set_data(self, data: str) -> str:
        if data is None or data == "":
            raise ValueError("{} is invalid".format(self.name))

        if not isinstance(data, str):
            raise TypeError("{} invalid Type".format(self.name))

        return data

    def set_status(self, status: bool) -> bool:
        if not isinstance(status, bool):
            raise TypeError("{} invalid Type".format(self.name))

        return status

    data_id = ndb.StringProperty(indexed=True, validator=set_id)
    data = ndb.PickleProperty(validator=set_data)
    status = ndb.BooleanProperty(default=True, validator=set_status)

    # TODO - finish this
