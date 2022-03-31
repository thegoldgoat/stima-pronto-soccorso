from enum import Enum
import mongoengine

from .patient_model import PatientModel


class EmergencyCode(Enum):
    RED = 0
    YELLOW = 1
    GREEN = 2


class WaitingPatientModel(mongoengine.Document):
    patientId = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    arrival_time = mongoengine.DateTimeField(required=True)
    emergency_code = mongoengine.EnumField(EmergencyCode)

    average = mongoengine.IntField(min_value=0, required=True)
    deviation = mongoengine.IntField(min_value=0, required=True)
