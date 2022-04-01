from datetime import datetime
import logging
from src.simulator.generators.gauss_generator import GaussGenerator
from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.common.patient import Patient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.ColorCode.color_constants import COLOR_GREEN, COLOR_YELLOW, COLOR_RED
from src.common.logging.logger import createLogginWithName
from src.simulator.simulation_manager import SimulationManager

import mongoengine
from src.common.Models.waiting_patient_model import WaitingPatientModel
from src.common.Models.therapy_patient_model import TherapyPatientModel
import math

logger = createLogginWithName('Main', logging.INFO)

N = 10000


def normalizeTime(time: datetime):
    delta = time - datetime.now()
    return math.ceil(delta.total_seconds()/60)


def main():
    mongoengine.connect("stima-pronto-soccorso")
    waiting_queues = WaitingQueue(3)

    for waiting_patient in WaitingPatientModel.objects:
        waiting_queues.push(
            Patient(
                str(waiting_patient.patient_id.pk),
                GaussGenerator(waiting_patient.average,
                               waiting_patient.deviation),
                # TODO get from db when implemented in the model
                ExponentialGenerator(1),
                waiting_patient.emergency_code.value,
                normalizeTime(waiting_patient.arrival_time)
            )
        )

    logger.info("Loaded {} patients in waiting queue".format(
        waiting_queues.get_patients_count()))

    therapy_patients_list = []
    # Add the patient currently in therapy_queue

    for therapy_patient in TherapyPatientModel.objects:
        therapy_patients_list.append(
            Patient(
                str(therapy_patient.pk),
                GaussGenerator(therapy_patient.average,
                               therapy_patient.deviation),
                # TODO get from db when implemented in the model
                ExponentialGenerator(1),
                None,
                normalizeTime(therapy_patient.entry_time)
            )
        )

    logger.info("Loaded {} patients in therapy state".format(
        len(therapy_patients_list)))

    simulation_manager = SimulationManager(
        waiting_queues, therapy_patients_list, N)
    simulation_manager.run_all_simulation_sync()
    simulation_manager.plot_all()
    simulation_manager.store_all()


if __name__ == '__main__':
    main()
