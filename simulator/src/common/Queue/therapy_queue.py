from src.common.therapy_patient import TherapyPatient
from src.common.Queue.my_priority_queue import MyPriorityQueue


class TherapyQueue():
    def __init__(self, max_size):
        self._max_size = max_size
        self.therapy_queue = MyPriorityQueue()

    def is_full(self):
        return len(self.therapy_queue.heap) == self._max_size

    def push(self, new_patient: TherapyPatient) -> None:
        """ Add patient to the therapy queue, if not full."""
        if self.is_full():
            raise Exception("Therapy queue is full")

        self.therapy_queue.push(new_patient)

    def peek(self) -> TherapyPatient:
        """ Get the minimum therapy time present in the therapy_queue """
        return self.therapy_queue.get_min()

    def pop(self) -> TherapyPatient:
        """ Return (and pop from the therapy_queue) the therapy patient that has the lowest therapy time (should be = 0)  """
        return self.therapy_queue.pop()

    def decrement_therapy_times(self, elapsed_time) -> None:
        """ Update the therapy time for each patient present in the therapy_queue """
        for therapy_patient in self.therapy_queue.heap:
            therapy_patient.decrement_therapy_time(elapsed_time)
