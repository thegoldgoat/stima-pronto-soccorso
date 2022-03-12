from typing import List
import queue

from src.common.patient import Patient


class Simulator():
    def __init__(self, priority_queues: List[queue.PriorityQueue], therapy_state: List[Patient]):

        self._priority_queues = priority_queues
        self._therapy_state = therapy_state

    def simulate(self):
        pass

    def _iteration(self):
        pass
