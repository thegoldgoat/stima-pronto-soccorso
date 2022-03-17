from src.common.Queue.waiting_queue import WaitingQueue
from src.common.Queue.therapy_queue import TherapyQueue


class Simulator():
    def __init__(self, waiting_queues: WaitingQueue, therapy_state: TherapyQueue):

        self._waiting_queues = waiting_queues
        self._therapy_state = therapy_state

    def simulate(self):
        print("Starting simulation!")

    def _iteration(self):
        pass
