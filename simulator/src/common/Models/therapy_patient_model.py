import re
import mongoengine
from requests import request

from .patient_model import PatientModel


class TherapyPatientModel(mongoengine.Document):
    patient_id = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)
    emergency_code = mongoengine.IntField(required=True)
    entry_time = mongoengine.DateTimeField(required=True)