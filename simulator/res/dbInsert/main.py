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
                emergency_code=esi,
                average=3+i,
                deviation=1+i
            ).save()

    patient = PatientModel().save()
    TherapyPatientModel(
        patient_id=patient,
        entry_time=datetime.now(),
        average=2,
        deviation=2
    ).save()

    patient = PatientModel().save()
    TherapyPatientModel(
        patient_id=patient,
        entry_time=datetime.now(),
        average=1,
        deviation=2
    ).save()


if __name__ == "__main__":
    mongoengine.connect("stima-pronto-soccorso")
    insertPatients()
