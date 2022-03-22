from typing import List
from src.simulator.generators.gauss_generator import GaussGenerator
from src.simulator.generators.exponential_generator import ExponentialGenerator
from src.common.patient import Patient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.ColorCode.color_constants import COLOR_GREEN, COLOR_YELLOW, COLOR_RED
from src.common.logging.logger import createLogginWithName
from src.simulator.simulation_manager import SimulationManager

logger = createLogginWithName('Main')

N = 1000


def main():
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

    simulation_manager = SimulationManager(waiting_queues, therapy_patients_list, N)
    simulation_manager.run_all_simulation_sync()
    simulation_manager.plot_all()


if __name__ == '__main__':
    main()
