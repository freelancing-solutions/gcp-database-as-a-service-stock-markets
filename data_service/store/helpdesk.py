from google.cloud import ndb
from datetime import datetime


class HelpDesk(ndb.Model):
    total_tickets: int = ndb.IntegerProperty(default=0)
    total_tickets_opened: int = ndb.IntegerProperty(default=0)
    total_tickets_closed: int = ndb.IntegerProperty(default=0)

    def __str__(self) -> str:
        return "<HelpDesk total_tickets: {}, total_open : {}, total_closed: {}".format(str(self.total_tickets),
                                                                                       str(self.total_tickets_closed),
                                                                                       str(self.total_tickets_opened))

    def __repr__(self) -> str:
        return self.__str__()

class Ticket(ndb.Model):
    ticket_id: str = ndb.StringProperty()
    uid: str = ndb.StringProperty()
    topic: str = ndb.StringProperty()
    subject: str = ndb.StringProperty()
    message: str = ndb.StringProperty()
    email: str = ndb.StringProperty()
    cell: str = ndb.StringProperty()
    assigned: bool = ndb.BooleanProperty(default=False)
    assigned_to_uid: str = ndb.StringProperty()
    response_sent: bool = ndb.BooleanProperty(default=False)
    is_resolved: bool = ndb.BooleanProperty(default=False)
    client_not_responding: bool = ndb.BooleanProperty(default=False)
    time_created: datetime = ndb.DateTimeProperty(auto_now_add=True)
    time_updated: datetime = ndb.DateTimeProperty(auto_now=True)

    def __eq__(self, other) -> bool:
        if self.__class__ != other.__class__:
            return False
        if self.ticket_id != other.ticket_id:
            return False
        return True

    def __str__(self) -> str:
        return "<Ticket topic: {}, subject: {}, message: {}, email: {}, cell: {}, is_resolved: {}".format(
            self.topic, self.subject, self.message, self.email, self.cell, self.is_resolved)

    def __repr__(self) -> str:
        return self.__str__()




