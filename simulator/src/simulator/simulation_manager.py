from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime
import logging
from threading import Lock
from typing import Dict, List
from src.simulator.generators.exponential_generator_time_variant import ExponentialGeneratorTimeVariant

from src.simulator.simulator import Simulator
from src.common.therapy_patient import TherapyPatient
from src.common.Queue.therapy_queue import TherapyQueue
from src.common.logging.logger import createLogginWithName
from src.common.patient import Patient
from src.common.Queue.waiting_queue import WaitingQueue
from src.common.Models.simulation_model import SimulationModel
from src.common.Models.esteem_model import EsteemModel
from src.common.EsiCodes.esi_constants import THERAPY_SIZE

import os

logger = createLogginWithName('SimulationManager', logging.ERROR)


class SimulationManager:
    '''
        Class that manages the simulations and aggregates the data
    '''

    def __init__(self, waiting_queues: WaitingQueue, therapy_patients_list: List[Patient], simulations_count: int, exponential_generators_time_variant: List[ExponentialGeneratorTimeVariant]):
        self._initial_waiting_queues = waiting_queues
        self._initial_therapy_patients_list = therapy_patients_list
        self._simulation_count = simulations_count
        self._exponential_generators_time_variant = exponential_generators_time_variant
        self.aggregated_results = {}
        self.lock = Lock()
    
    def _clone_current_datetime(self, current_datetime: datetime):
        '''
            Returns a copy of the current datetime.
        '''
        
        return datetime(current_datetime.year, current_datetime.month, current_datetime.day, current_datetime.hour, current_datetime.minute)
    
    
    def run_all_simulation_sync(self):      
        current_datetime = datetime.now()  
        with ThreadPoolExecutor() as executor:
            my_futures = [executor.submit(
                self._run_and_aggregate_single_simulation, current_datetime) for _ in range(self._simulation_count)]
            wait(my_futures)

    def _run_and_aggregate_single_simulation(self, current_datetime: datetime):
        simulator_result = self._run_single_simulation(current_datetime)

        self.lock.acquire()
        self._aggregate_single_result(simulator_result)
        self.lock.release()

    def _aggregate_single_result(self, simulation_result: Dict[int, int]):
        for patient_id, waiting_time in simulation_result.items():
            if patient_id not in self.aggregated_results:
                self.aggregated_results[patient_id] = {waiting_time: 1}
            else:
                current_patient_waiting_times = self.aggregated_results[patient_id]
                if waiting_time not in current_patient_waiting_times:
                    self.aggregated_results[patient_id][waiting_time] = 1
                else:
                    self.aggregated_results[patient_id][waiting_time] += 1

    def _run_single_simulation(self, current_datetime: datetime):
        logger.debug("Launching simulation preparation")

        waiting_queues_copy = self._initial_waiting_queues.create_copy_and_generate()

        therapy_queue = TherapyQueue(THERAPY_SIZE)
        
        for therapy_patient in self._initial_therapy_patients_list:
            therapy_queue.push(TherapyPatient(therapy_patient.id,
                                              therapy_patient.therapy_generator
                                              ))
        
        copy_of_current_datetime = self._clone_current_datetime(current_datetime)
        
        simulator = Simulator(waiting_queues_copy, therapy_queue, self._exponential_generators_time_variant, copy_of_current_datetime)

        try:
            result = simulator.simulate()
        except Exception as e:
            # Print exception message even if it's raised in a thread
            logger.exception("Exception in simulator")

        logger.info('Simulation ended in %s iterations',
                    simulator.iteration_count)

        return result

    def plot_all(self, base_path="output/simulation/"):
        '''
            Plots all the results of the simulation
        '''

        if not os.path.exists(base_path):
            os.makedirs(base_path)

        import matplotlib.pyplot as plt

        for patient_id, waiting_times in self.aggregated_results.items():

            x_values = [val[0] for val in waiting_times.items()]
            y_values = [
                val[1] / self._simulation_count for val in waiting_times.items()]

            plt.clf()
            plt.stem(x_values, y_values, linefmt='blue', markerfmt=" ")
            plt.xlabel("Waiting time in minutes")
            plt.ylabel("Occurrences Percentage")
            plt.title(
                f"Results for {self._simulation_count} simulations", fontsize=10)
            plt.suptitle(f"Patient {patient_id}")

            plt.savefig('{0}patient{1}.png'.format(base_path, patient_id))

    def store_all(self):
        simulation = SimulationModel(simulation_time=datetime.now()).save()
        for patient_id, waiting_times in self.aggregated_results.items():
            normalized_waiting_times = {}
            for (time, occurrence) in waiting_times.items():
                normalized_waiting_times[str(
                    time)] = occurrence/self._simulation_count
            EsteemModel(simulation_id=simulation, patient_id=patient_id,
                        waiting_times=normalized_waiting_times).save()