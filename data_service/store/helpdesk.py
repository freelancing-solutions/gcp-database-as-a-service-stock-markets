from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError

class HelpDesk(ndb.Model):
    total_tickets: int = ndb.IntegerProperty(default=0)
    total_tickets_opened: int = ndb.IntegerProperty(default=0)
    total_tickets_closed: int = ndb.IntegerProperty(default=0)



