from concurrent.futures import ThreadPoolExecutor, wait
from queue import PriorityQueue

from .generators.gauss_generator import GaussGenerator
from .generators.exponential_generator import ExponentialGenerator
from .simulator import Simulator

from src.common.patient import Patient

from src.common.waiting_queue import WaitingQueue


def run_single_simulation(waiting_queues: WaitingQueue):
    waiting_queues_copy = waiting_queues.create_copy_and_generate()

    print('Initial')
    print(waiting_queues)
    print('Copy')
    print(waiting_queues_copy)


CODE_RED = 0
CODE_YELLOW = 1
CODE_GREEN = 2
CODE_COUNT = 3

N = 10


def main():
    print("Hello simulator!")

    waiting_queues = WaitingQueue(CODE_COUNT)

    waiting_queues.put(Patient(GaussGenerator(2, 2),
                               ExponentialGenerator(2), CODE_RED, 0))
    waiting_queues.put(Patient(GaussGenerator(3, 1),
                               ExponentialGenerator(3), CODE_RED, 0))
    waiting_queues.put(Patient(GaussGenerator(4, 5),
                               ExponentialGenerator(1), CODE_RED, 0))

    waiting_queues.put(Patient(GaussGenerator(
        2, 2), ExponentialGenerator(2), CODE_YELLOW, 0))
    waiting_queues.put(Patient(GaussGenerator(
        3, 1), ExponentialGenerator(3), CODE_YELLOW, 0))
    waiting_queues.put(Patient(GaussGenerator(
        4, 5), ExponentialGenerator(1), CODE_YELLOW, 0))

    waiting_queues.put(Patient(GaussGenerator(2, 2),
                               ExponentialGenerator(2), CODE_GREEN, 0))
    waiting_queues.put(Patient(GaussGenerator(3, 1),
                               ExponentialGenerator(3), CODE_GREEN, 0))
    waiting_queues.put(Patient(GaussGenerator(4, 5),
                               ExponentialGenerator(1), CODE_GREEN, 0))

    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(
            run_single_simulation, waiting_queues) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    main()
