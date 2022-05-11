import logging
from typing import List
from src.common.Queue.interarrival_queue import InterarrivalQueue
from src.common.patient import Patient
from src.common.therapy_patient import TherapyPatient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.Queue.therapy_queue import TherapyQueue
from src.common.EsiCodes.esi_constants import ESI_GAUSSIANS, ESI_LEAVE
from src.common.logging.logger import createLogginWithName
from src.simulator.generators.exponential_generator_time_variant import ExponentialGeneratorTimeVariant
from datetime import datetime, timedelta


logger = createLogginWithName('Simulator')

class Simulator():
    def __init__(self, waiting_queues: WaitingQueue, therapy_state: TherapyQueue, exponential_generators_time_variant: List[ExponentialGeneratorTimeVariant], current_datetime: datetime):
        self._waiting_queues = waiting_queues
        self._therapy_state = therapy_state
        self._datetime_in_simulation = current_datetime
        self._interarrive_state = InterarrivalQueue(exponential_generators_time_variant, current_datetime)

    def simulate(self):
        '''
            Returns a Dict whose key is the Patient ID, while the value is
            the time it took for it to be moved in therapy
        '''
        logger.info("Starting simulation")

        self.current_time = 0
        self.result_dict = dict()
        self.total_initial_patients_in_queue = self._waiting_queues.get_patients_count()
        
        self.moved_in_therapy_patients = 0

        self.iteration_count = 0

        # Move as many patient from waiting to therapy as you can
        while self._therapy_state.is_full() is False:
            logger.debug("Therapy not full. Automatically fill it")
            self._move_from_waiting_to_therapy()

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
        self.iteration_count += 1

        logger.debug("Iteration %s", self.iteration_count)
        logger.debug("Moved patients / Initial patients : %s / %s",
                     self.moved_in_therapy_patients, self.total_initial_patients_in_queue)

        minimum_therapy = self._therapy_state.peek()
        minimum_interarrive = self._interarrive_state.peek()

        # TODO: Leave times

        if minimum_therapy.therapy_time < minimum_interarrive[1]:
            # Therapy is minimum
            logger.debug("Therapy leave event: Patient ID=%s",
                         minimum_therapy.id)
            time_elapsed = minimum_therapy.therapy_time

            self.current_time += time_elapsed
            # Update datetime of simulation
            self._datetime_in_simulation += timedelta(seconds=time_elapsed*60)
            
            self._therapy_state.pop()

            self._therapy_state.decrement_therapy_times(time_elapsed)
            self._interarrive_state.decrement_interarrive(time_elapsed)

            self._move_from_waiting_to_therapy()

        else:
            # Interarrive is minimum
            logger.debug("Interarrive event: ESI Code=%d",
                         minimum_interarrive[0])

            esi_code = minimum_interarrive[0]
            time_elapsed = minimum_interarrive[1]

            self.current_time += time_elapsed
            self._datetime_in_simulation += timedelta(seconds=time_elapsed*60)

            new_patient = Patient("", ESI_GAUSSIANS[esi_code-1],
                                  ESI_LEAVE[esi_code-1], esi_code, self._datetime_in_simulation)

            new_patient.generate_leave()

            self._waiting_queues.push(new_patient)

            self._therapy_state.decrement_therapy_times(time_elapsed)
            
            self._interarrive_state.pop_regenerate_decrement_others(self._datetime_in_simulation)

    def _move_from_waiting_to_therapy(self):
        # Move one patient from the waiting queue to therapy
        patient_to_move = self._waiting_queues.pop()

        if patient_to_move.id != "":
            # Patient is real, their waiting time is finished
            self.result_dict[patient_to_move.id] = self.current_time
            self.moved_in_therapy_patients += 1

        therapy_patient_to_move = TherapyPatient(
            patient_to_move.id,
            patient_to_move.therapy_generator,
            patient_to_move.therapy_time
        )

        self._therapy_state.push(therapy_patient_to_move)