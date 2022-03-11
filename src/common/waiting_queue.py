from queue import PriorityQueue
from .patient import Patient


class WaitingQueue():
    def __init__(self, queues_count: int):
        self.priority_queues = [PriorityQueue() for _ in range(queues_count)]

    def put(self, new_patient: Patient):
        priority_code = new_patient.emergency_code

        # Add new patient to the corresponding queue
        self.priority_queues[priority_code].put(
            (new_patient.arrival_time, new_patient)
        )

    def create_copy_and_generate(self):
        # TODO create a shallow copy, generate variabili aleatorie and return
        pass
