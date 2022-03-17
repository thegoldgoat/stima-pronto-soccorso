from typing import Dict
from unittest import result
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.Queue.therapy_queue import TherapyQueue


class Simulator():
    def __init__(self, waiting_queues: WaitingQueue, therapy_state: TherapyQueue):
        self._waiting_queues = waiting_queues
        self._therapy_state = therapy_state

    def simulate(self):
        '''
            Returns a Dict whose key is the Patient ID, while the value is
            the time it took for it to be moved in therapy
        '''
        print("Starting simulation!")

        self.current_time = 0
        self.result_dict = Dict()
        self.total_initial_patients_in_queue = self._waiting_queues.get_patients_count()

        self.moved_in_therapy_patients = 0

        while self.moved_in_therapy_patients != self.total_initial_patients_in_queue:
            self._iteration()

        return self.result_dict

    def _iteration(self):
        '''
            Do an iteration:

            1. Find minimum sample between therapy, leave (TODO?) and inter-arrive
            2. Update current_time based on the minimum value
            3.  If minimum is therapy, move a patient from the waiting queue
                    to therapy (if the patient is real, add them to the self.result_dict
                    and increment moved_in_therapy_patients)
                If the minimum is inter-arrive, add a new patient to the waiting_queue
                (TODO) If the minimum is leave, remove that patient from the waiting_queue
            4. Update timing for each value in the waiting_queues, therapy_state, and
                leave_time
        '''
        pass
