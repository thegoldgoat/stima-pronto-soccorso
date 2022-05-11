from enum import Enum
import re
import mongoengine

class TherapyTimesOccurrencesModel(mongoengine.Document):
    emergency_code = mongoengine.IntField(required=True)
    therapy_time = mongoengine.IntField(required=True)
    occurrences = mongoengine.IntField(required=True)