from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, UTCDateTimeAttribute

class Log(Model):
    class Meta:
        table_name = 'zappa-playground-logs'

    name = UnicodeAttribute(hash_key=True)
    ip_address = UnicodeAttribute()
    timestamp = UTCDateTimeAttribute()

    def say(self):
        print('hello')
