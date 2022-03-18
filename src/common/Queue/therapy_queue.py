from src.common.therapy_patient import TherapyPatient
from .my_priority_queue import MyPriorityQueue


class TherapyQueue():
    def __init__(self):
        self.therapy_queue = MyPriorityQueue()

    def push(self, new_patient: TherapyPatient):
        """ Add patient to the therapy queue """
        self.therapy_queue.push(new_patient)

    def peak(self):
        """ Get the minimum therapy time present in the therapy_queue """
        return self.therapy_queue.get_min()

    def pop(self):
        """ Return (and pop from the therapy_queue) the therapy patient that has the lowest therapy time (should be = 0)  """
        return self.therapy_queue.pop()

    def decrement_therapy_times(self, elapsed_time):
        """ Update the therapy time for each patient present in the therapy_queue """
        for therapy_patient in self.therapy_queue.heap:
            therapy_patient.decrement_therapy_time(elapsed_time)