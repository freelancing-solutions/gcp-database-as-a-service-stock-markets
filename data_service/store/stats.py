from google.cloud import ndb
from data_service.utils.utils import timestamp


class ClientTraffic(ndb.Model):
    """
        use hooks on client app, to update this stats....
        expose endpoints to increment statistics on an interval say minute interval
        there should be a task running which will call the client endpoint holding the stats
        and then take the data and store here
        ...
        the admin app should be able to call the exposed endpoint to fetch data
        the cache may not store this data as it will be fetched on an interval by admin app
    """
    interval_id: str = ndb.StringProperty()
    total_requests: int = ndb.IntegerProperty(default=0)
    average_requests_per_second: int = ndb.IntegerProperty(default=0)
    interval_epoch: int = ndb.IntegerProperty(default=timestamp())

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.interval_id != other.interval_id:
            return False
        if self.total_requests != other.total_requests:
            return False
        if self.interval_epoch != other.interval_epoch:
            return False
        return True

    def __str__(self) -> str:
        return "{} {} {}".format(str(self.total_requests), str(self.average_requests_per_second),
                                 str(self.interval_epoch))

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        if self.interval_id:
            return 1
        return 0


class DataServiceTraffic(ndb.Model):
    """
        use hooks on data-service app to update this stats
    """
    interval_id: str = ndb.StringProperty()
    total_requests: int = ndb.IntegerProperty(default=0)
    average_requests_per_second: int = ndb.IntegerProperty(default=0)
    interval_epoch: int = ndb.IntegerProperty(default=timestamp())

    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        if self.interval_id != other.interval_id:
            return False
        if self.interval_epoch != other.interval_epoch:
            return False
        return True

    def __str__(self):
        return "{} {} {}".format(str(self.total_requests), str(self.average_requests_per_second),
                                 str(self.interval_epoch))

    def __repr__(self):
        return self.__str__()

    def __len__(self) -> int:
        if self.interval_id:
            return 1
        return 0
