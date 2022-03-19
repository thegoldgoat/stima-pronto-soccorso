from src.common.therapy_patient import TherapyPatient
from .my_priority_queue import MyPriorityQueue


class TherapyQueue():
    def __init__(self, heap=None, bool_heapify=False):
        self.therapy_queue = MyPriorityQueue(heap, bool_heapify)

    def push(self, new_patient: TherapyPatient):
        """ Add patient to the therapy queue """
        self.therapy_queue.push(new_patient)

    # TODO: Safe remove (?)
    def create_copy_and_generate(self):
        """ Create a deep copy, generate random variables and return """
        return_value = TherapyQueue()
        return_value.therapy_queue = MyPriorityQueue(
            heap=[therapyPatient.clone_and_generate() for therapyPatient in self.therapy_queue.heap])

        return return_value
