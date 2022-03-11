from asyncio import futures
from concurrent.futures import ThreadPoolExecutor, wait
from common.patient import Patient
from simulator.generators.gauss_generator import GaussGenerator
from simulator.generators.exponential_generator import ExponentialGenerator
from src.simulator.simulator import Simulator
from queue import PriorityQueue


def run_single_simulation(priority_queues):
    # TODO Instantiate deep copy with PatientSimulator instead of Patient
    pass


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
        2, 2), ExponentialGenerator(2), CODE_RED, 0))
    yellow_queue.add(Patient(GaussGenerator(
        3, 1), ExponentialGenerator(3), CODE_RED, 0))
    yellow_queue.add(Patient(GaussGenerator(
        4, 5), ExponentialGenerator(1), CODE_RED, 0))

    green_queue = PriorityQueue()
    green_queue.add(Patient(GaussGenerator(2, 2),
                    ExponentialGenerator(2), CODE_RED, 0))
    green_queue.add(Patient(GaussGenerator(3, 1),
                    ExponentialGenerator(3), CODE_RED, 0))
    green_queue.add(Patient(GaussGenerator(4, 5),
                    ExponentialGenerator(1), CODE_RED, 0))

    priority_queues = [
        red_queue, yellow_queue, green_queue
    ]

    with ThreadPoolExecutor() as executor:

        my_futures = [executor.submit(
            run_single_simulation, priority_queues) for _ in range(N)]
        wait(my_futures)


if __name__ == '__main__':
    main()
