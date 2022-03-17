from concurrent.futures import ThreadPoolExecutor, wait
from queue import PriorityQueue

from pyrsistent import v

from common.Queue.therapy_queue import TherapyQueue, therapy_queue
from common.therapyPatient import TherapyPatient

from .generators.gauss_generator import GaussGenerator
from .generators.exponential_generator import ExponentialGenerator
from .simulator import Simulator

from src.common.patient import Patient

from src.common.Queue.waiting_queue import WaitingQueue


def run_single_simulation(waiting_queues: WaitingQueue, therapy_queue: TherapyQueue):
    waiting_queues_copy = waiting_queues.create_copy_and_generate()

    therapy_queue_copy = therapy_queue.create_copy_and_generate()


CODE_RED = 0
CODE_YELLOW = 1
CODE_GREEN = 2
CODE_COUNT = 3

N = 1


def main():
    print("Hello simulator!")

    waiting_queues = WaitingQueue(CODE_COUNT)

    waiting_queues.push(Patient(0, GaussGenerator(2, 2),
                                ExponentialGenerator(2), CODE_RED, 0))

    waiting_queues.push(Patient(1, GaussGenerator(3, 1),
                                ExponentialGenerator(3), CODE_RED, 0))

    waiting_queues.push(Patient(2, GaussGenerator(4, 5),
                                ExponentialGenerator(1), CODE_RED, 0))

    waiting_queues.push(Patient(3, GaussGenerator(
        2, 2), ExponentialGenerator(2), CODE_YELLOW, 0))

    waiting_queues.push(Patient(4, GaussGenerator(
        3, 1), ExponentialGenerator(3), CODE_YELLOW, 0))

    waiting_queues.push(Patient(5, GaussGenerator(
        4, 5), ExponentialGenerator(1), CODE_YELLOW, 0))

    waiting_queues.push(Patient(6, GaussGenerator(2, 2),
                                ExponentialGenerator(2), CODE_GREEN, 0))

    waiting_queues.push(Patient(7, GaussGenerator(3, 1),
                                ExponentialGenerator(3), CODE_GREEN, 0))

    waiting_queues.push(Patient(8, GaussGenerator(4, 5),
                                ExponentialGenerator(1), CODE_GREEN, 0))

    therapy_queue = therapy_queue()
    # Add the patient currently in therapy_queue

    therapy_queue.push(TherapyPatient(9, GaussGenerator(4, 5)))

    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(
            run_single_simulation, waiting_queues, therapy_queue) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    main()
