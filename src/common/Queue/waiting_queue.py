from ..patient import Patient
from .my_priority_queue import MyPriorityQueue


class WaitingQueue():
    def __init__(self, queues_count: int):
        self.priority_queues = [MyPriorityQueue() for _ in range(queues_count)]

    def push(self, new_patient: Patient):
        priority_code = new_patient.emergency_code

        # Add new patient to the corresponding queue
        self.priority_queues[priority_code].push(new_patient)

    def create_copy_and_generate(self):
        # create a deep copy, generate variabili aleatorie and return
        return_value = WaitingQueue(0)

        copy_queues = [
            MyPriorityQueue(
                heap=[patient.clone_and_generate() for patient in queue.heap]
            )
            for queue in self.priority_queues
        ]

        return_value.priority_queues = copy_queues

        return return_value
