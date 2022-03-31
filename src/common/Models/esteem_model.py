import mongoengine

from .patient_model import PatientModel

class EsteemModel(mongoengine.Document):
    patientId = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    waiting_times = mongoengine.DictField(required=True)