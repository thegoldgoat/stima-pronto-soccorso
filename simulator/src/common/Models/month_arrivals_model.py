from enum import Enum
import re
import mongoengine


class EmergencyCode(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2

class MonthArrivals(mongoengine.Document):
    emergency_code = mongoengine.EnumField(EmergencyCode, required=True)
    month = mongoengine.IntField(required=True)
    year = mongoengine.IntField(required=True)
    arrivals = mongoengine.IntField(required=True)