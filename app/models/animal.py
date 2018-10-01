from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute


class Animal(Model):
    class Meta:
        table_name = 'zappa-playground-animals'
        region = 'ap-northeast-1'

    family = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
