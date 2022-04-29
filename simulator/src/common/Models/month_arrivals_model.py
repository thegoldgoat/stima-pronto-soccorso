from enum import Enum
import re
import mongoengine

class MonthArrivals(mongoengine.Document):
    emergency_code = mongoengine.IntField(required=True)
    month = mongoengine.IntField(required=True)
    year = mongoengine.IntField(required=True)
    arrivals = mongoengine.IntField(required=True)