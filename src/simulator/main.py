from concurrent.futures import ThreadPoolExecutor, wait
from queue import PriorityQueue

from generators.gauss_generator import GaussGenerator
from generators.exponential_generator import ExponentialGenerator
from simulator import Simulator

from src.common.patient import Patient
from src.common.patient_simulator import PatientSimulator


def run_single_simulation(priority_queues):
    # Instantiate deep copy with PatientSimulator instead of Patient

    # Meaning of the next line
    # priority_queues_copy = [
    #     map(lambda input_patient: PatientSimulator(input_patient),
    #         initial_queue) for initial_queue in priority_queues
    # ]

    priority_queues_copy = map(
        lambda initial_queue:
            map(lambda input_patient: PatientSimulator(
                input_patient), initial_queue),
        priority_queues
    )

    print('Initial')
    print(priority_queues)
    print('Copy')
    print(priority_queues_copy)


CODE_RED = 0
CODE_YELLOW = 1
CODE_GREEN = 2

N = 10


def main():
    print("Hello simulator!")

    red_queue = PriorityQueue()
    red_queue.add(Patient(GaussGenerator(2, 2),
                  ExponentialGenerator(2), CODE_RED, 0))
    red_queue.add(Patient(GaussGenerator(3, 1),
                  ExponentialGenerator(3), CODE_RED, 0))
    red_queue.add(Patient(GaussGenerator(4, 5),
                  ExponentialGenerator(1), CODE_RED, 0))

    yellow_queue = PriorityQueue()
    yellow_queue.add(Patient(GaussGenerator(
        2, 2), ExponentialGenerator(2), CODE_YELLOW, 0))
    yellow_queue.add(Patient(GaussGenerator(
        3, 1), ExponentialGenerator(3), CODE_YELLOW, 0))
    yellow_queue.add(Patient(GaussGenerator(
        4, 5), ExponentialGenerator(1), CODE_YELLOW, 0))

    green_queue = PriorityQueue()
    green_queue.add(Patient(GaussGenerator(2, 2),
                    ExponentialGenerator(2), CODE_GREEN, 0))
    green_queue.add(Patient(GaussGenerator(3, 1),
                    ExponentialGenerator(3), CODE_GREEN, 0))
    green_queue.add(Patient(GaussGenerator(4, 5),
                    ExponentialGenerator(1), CODE_GREEN, 0))

    priority_queues = [
        red_queue, yellow_queue, green_queue
    ]

    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(
            run_single_simulation, priority_queues) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    main()
