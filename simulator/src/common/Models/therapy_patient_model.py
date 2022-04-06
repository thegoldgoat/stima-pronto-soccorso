import mongoengine

from .patient_model import PatientModel


class TherapyPatientModel(mongoengine.Document):
    patient_id = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    entry_time = mongoengine.DateTimeField(required=True)

    average = mongoengine.IntField(min_value=0, required=True)
    deviation = mongoengine.IntField(min_value=0, required=True)
