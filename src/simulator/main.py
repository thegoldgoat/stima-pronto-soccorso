from concurrent.futures import ThreadPoolExecutor, wait
from typing import List
from src.common.therapy_patient import TherapyPatient
from src.common.Queue.therapy_queue import TherapyQueue
from src.simulator.generators.gauss_generator import GaussGenerator
from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.simulator.simulator import Simulator
from src.common.patient import Patient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.ColorCode.color_constants import COLOR_GREEN, COLOR_YELLOW, COLOR_RED
from src.common.logging.logger import createLogginWithName
from src.simulator.plotting import Plotting

logger = createLogginWithName('Main')

N = 10000

def run_single_simulation(waiting_queues: WaitingQueue, therapy_patients_list: List[Patient]):
    logger.debug("Launching simulation preparation")

    waiting_queues_copy = waiting_queues.create_copy_and_generate()

    therapy_queue = TherapyQueue(2)

    for therapy_patient in therapy_patients_list:
        therapy_queue.push(TherapyPatient(therapy_patient.id,
                                          therapy_patient.therapy_generator
                                          ))

    simulator = Simulator(waiting_queues_copy, therapy_queue)

    try:
        result = simulator.simulate()
    except Exception as e:
        # Print exception message even if it's raised in a thread
        logger.exception("Exception in simulator")

    logger.info('Simulation ended in %s iterations',
                simulator.iteration_count)
    for (patient_id, waiting_time) in result.items():
        logger.debug('ID={0}\tTime={1}'.format(patient_id, waiting_time))

    return result


def main(plotting):
    waiting_queues = WaitingQueue(3)

    waiting_queues.push(Patient(0, GaussGenerator(2, 2),
                                ExponentialGenerator(2), COLOR_RED, 0))

    waiting_queues.push(Patient(1, GaussGenerator(3, 1),
                                ExponentialGenerator(3), COLOR_RED, 1))

    waiting_queues.push(Patient(2, GaussGenerator(4, 5),
                                ExponentialGenerator(1), COLOR_RED, 2))

    waiting_queues.push(Patient(3, GaussGenerator(
        2, 2), ExponentialGenerator(2), COLOR_YELLOW, 0))

    waiting_queues.push(Patient(4, GaussGenerator(
        3, 1), ExponentialGenerator(3), COLOR_YELLOW, 1))

    waiting_queues.push(Patient(5, GaussGenerator(
        4, 5), ExponentialGenerator(1), COLOR_YELLOW, 2))

    waiting_queues.push(Patient(6, GaussGenerator(2, 2),
                                ExponentialGenerator(2), COLOR_GREEN, 0))

    waiting_queues.push(Patient(7, GaussGenerator(3, 1),
                                ExponentialGenerator(3), COLOR_GREEN, 1))

    waiting_queues.push(Patient(8, GaussGenerator(1, 1),
                                ExponentialGenerator(1), COLOR_GREEN, 2))

    therapy_patients_list = []
    # Add the patient currently in therapy_queue

    therapy_patients_list.append(Patient(9, GaussGenerator(4, 5),
                                         ExponentialGenerator(3), COLOR_YELLOW, 1))
    
    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(plotting.collect_results,
            run_single_simulation, waiting_queues, therapy_patients_list) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    plotting = Plotting()
    main(plotting)
    plotting.plot_occurrences(N)