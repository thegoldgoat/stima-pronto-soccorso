from datetime import datetime
import mongoengine
from src.common.Models.patient_model import PatientModel
from src.common.Models.waiting_patient_model import WaitingPatientModel
from src.common.Models.therapy_patient_model import TherapyPatientModel
from src.common.ColorCode import color_constants


def insertPatients():
    for i in range(1, 3):
        patient = PatientModel().save()
        WaitingPatientModel(
            patient_id=patient,
            arrival_time=datetime.now(),
            emergency_code=color_constants.COLOR_RED,
            average=3+i,
            deviation=i
        ).save()
    for i in range(1, 3):
        patient = PatientModel().save()
        WaitingPatientModel(
            patient_id=patient,
            arrival_time=datetime.now(),
            emergency_code=color_constants.COLOR_YELLOW,
            average=2+i,
            deviation=i
        ).save()
    for i in range(1, 3):
        patient = PatientModel().save()
        WaitingPatientModel(
            patient_id=patient,
            arrival_time=datetime.now(),
            emergency_code=color_constants.COLOR_GREEN,
            average=1,
            deviation=i
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
