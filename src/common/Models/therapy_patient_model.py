import mongoengine

from .patient_model import PatientModel

class TherapyPatientModel(mongoengine.Document):
    patientId = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    arrival_time = mongoengine.DateTimeField(required=True)