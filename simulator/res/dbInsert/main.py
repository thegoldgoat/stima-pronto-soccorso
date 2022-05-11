from datetime import datetime
import mongoengine
from src.common.Models.patient_model import PatientModel
from src.common.Models.waiting_patient_model import WaitingPatientModel
from src.common.Models.therapy_patient_model import TherapyPatientModel
from src.common.EsiCodes import esi_constants

num_of_waiting_patients = 3

def insertPatients():
    for esi in esi_constants.ESI_CODES:
        for i in range(0, num_of_waiting_patients):
            patient = PatientModel().save()
            WaitingPatientModel(
                patient_id=patient,
                arrival_time=datetime.now(),
                emergency_code=esi
            ).save()

    patient = PatientModel().save()
    TherapyPatientModel(
        patient_id=patient,
        emergency_code=4,
        entry_time=datetime.now()
    ).save()

    patient = PatientModel().save()
    TherapyPatientModel(
        patient_id=patient,
        emergency_code=2,
        entry_time=datetime.now()
    ).save()


if __name__ == "__main__":
    mongoengine.connect("stima-pronto-soccorso")
    insertPatients()
