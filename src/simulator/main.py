from concurrent.futures import ThreadPoolExecutor, wait
from queue import PriorityQueue

from pyrsistent import v

from common.Queue.therapy_queue import TherapyQueue
from common.therapyPatient import TherapyPatient

from .generators.gauss_generator import GaussGenerator
from .generators.exponential_generator import ExponentialGenerator
from .simulator import Simulator

from src.common.patient import Patient

from src.common.Queue.waiting_queue import WaitingQueue


def run_single_simulation(waiting_queues: WaitingQueue):
    waiting_queues_copy = waiting_queues.create_copy_and_generate()

    print('Initial')
    print(waiting_queues.priority_queues[0].get_min().arrival_time)

    waiting_queues_copy.priority_queues[0].heap[0].arrival_time = '123'

    print('After assignment')
    print(waiting_queues.priority_queues[0].get_min().arrival_time)

    print('After assignment, on the copy')
    print(waiting_queues_copy.priority_queues[0].get_min().arrival_time)

    print('Generated therapy time on the source (should not be found)')
    try:
        print(waiting_queues.priority_queues[0].get_min().therapy_time)
    except:
        print('OK, not found.')

    print('Generated therapy time on the copy (should be 12345)')
    print(waiting_queues_copy.priority_queues[0].get_min().therapy_time)


CODE_RED = 0
CODE_YELLOW = 1
CODE_GREEN = 2
CODE_COUNT = 3

N = 1


def main():
    print("Hello simulator!")
    id = 0

    waiting_queues = WaitingQueue(CODE_COUNT)

    waiting_queues.push(Patient(id, GaussGenerator(2, 2),
                                ExponentialGenerator(2), CODE_RED, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(3, 1),
                                ExponentialGenerator(3), CODE_RED, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(4, 5),
                                ExponentialGenerator(1), CODE_RED, 0))

    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(
        2, 2), ExponentialGenerator(2), CODE_YELLOW, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(
        3, 1), ExponentialGenerator(3), CODE_YELLOW, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(
        4, 5), ExponentialGenerator(1), CODE_YELLOW, 0))

    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(2, 2),
                                ExponentialGenerator(2), CODE_GREEN, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(3, 1),
                                ExponentialGenerator(3), CODE_GREEN, 0))
    id += 1
    waiting_queues.push(Patient(id, GaussGenerator(4, 5),
                                ExponentialGenerator(1), CODE_GREEN, 0))

    therapyQueue = TherapyQueue()
    # Add the patient currently in therapyQueue
    id += 1
    therapyQueue.push(TherapyPatient(id, GaussGenerator(4, 5)))

    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(
            run_single_simulation, waiting_queues) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    main()
