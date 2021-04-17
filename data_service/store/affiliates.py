from google.cloud import ndb
from google.cloud.ndb.exceptions import BadArgumentError, BadQueryError, BadRequestError, BadValueError


class Affiliates(ndb.Model):
    affiliate_id = ndb.StringProperty()
    uid = ndb.StringProperty()

