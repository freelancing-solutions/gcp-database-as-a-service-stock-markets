from google.cloud import ndb


class Stock(ndb.Model):
    exchange_name = ndb.StringProperty()
    symbol = ndb.StringProperty()
    low = ndb.IntegerProperty(default=0)
    high = ndb.IntegerProperty(default=0)
    date = ndb.DateTimeProperty()

