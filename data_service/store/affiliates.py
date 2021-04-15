from google.cloud import ndb


class Affiliates(ndb.Model):
    affiliate_id = ndb.StringProperty()
    uid = ndb.StringProperty()

