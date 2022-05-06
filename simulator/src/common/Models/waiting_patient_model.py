import mongoengine

from .patient_model import PatientModel
   


class WaitingPatientModel(mongoengine.Document):
    patient_id = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    arrival_time = mongoengine.DateTimeField(required=True)
    emergency_code = mongoengine.IntField()

    average = mongoengine.IntField(min_value=0, required=True)
    deviation = mongoengine.IntField(min_value=0, required=True)
