import mongoengine

from .patient_model import PatientModel
   


class WaitingPatientModel(mongoengine.Document):
    patient_id = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)
    emergency_code = mongoengine.IntField()
    arrival_time = mongoengine.DateTimeField(required=True)