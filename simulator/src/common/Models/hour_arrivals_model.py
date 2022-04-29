from enum import Enum
import re
import mongoengine


class EmergencyCode(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2

class HourArrivals(mongoengine.Document):
    emergency_code = mongoengine.EnumField(EmergencyCode, required=True)
    year = mongoengine.IntField(required=True)
    day_in_week = mongoengine.IntField(required=True)
    hours_interval = mongoengine.StringField(required = True)
    arrivals_compared_to_average = mongoengine.IntField(required=True)