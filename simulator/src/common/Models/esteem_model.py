import mongoengine

from .patient_model import PatientModel
from .simulation_model import SimulationModel


class EsteemModel(mongoengine.Document):
    patient_id = mongoengine.ReferenceField(
        PatientModel, reverse_delete_rule=mongoengine.CASCADE)

    waiting_times = mongoengine.DictField(required=True)

    simulation_id = mongoengine.ReferenceField(SimulationModel)
