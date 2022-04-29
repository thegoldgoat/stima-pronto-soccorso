from enum import Enum
import re
import mongoengine


class HourArrivalsModel(mongoengine.Document):
    emergency_code = mongoengine.IntField(required=True)
    year = mongoengine.IntField(required=True)
    day_in_week = mongoengine.IntField(required=True)
    hours_interval = mongoengine.StringField(required = True)
    arrivals_compared_to_average = mongoengine.DecimalField(precision=3, required=True)