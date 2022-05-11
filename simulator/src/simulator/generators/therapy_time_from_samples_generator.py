
from datetime import timedelta
import random
from src.simulator.generators.generator import Generator
import numpy as np


class TherapyTimeFromSampleGenerator(Generator):

    def __init__(self, therapy_times_for_esi):
        """ This receives a list with therapy time and the times the terapy time has occured.
            I sort this list and I will take a value from therapy times (with weight algorithm)
            to assign the therapy time to the patient.
            If a patient was already in therapy when simulation started, the therapy time must be greater than
            the time he has already spent in therapy. To skip the lower values I sort the therapy times (done only once)
            and I grab the greater values. """

        therapy_times_for_esi = sorted(therapy_times_for_esi, key= lambda tuple: tuple[0]) # Sort by first value

        self.therapy_times = []
        self.therapy_times_occurrences = []
        for therapy_time_row in therapy_times_for_esi:
            self.therapy_times.append(therapy_time_row[0])
            self.therapy_times_occurrences.append(therapy_time_row[1])

    def generate_sample(self):
        return random.choices(self.therapy_times, weights=self.therapy_times_occurrences, k=1)[0]

    def generate_sample_with_minimum_value(self, minimum_value: int):
        if minimum_value > self.therapy_times[-1]:
            return minimum_value + 1 # It's greater than all known therapy times
        
        # Search index of first greater than minimum_value
        index = 0
        for i in range(0, len(self.therapy_times)):
            if self.therapy_times[i] > minimum_value:
                index = i
                break

        return random.choices(self.therapy_times[index:], weights=self.therapy_times_occurrences[index:], k=1)[0]
