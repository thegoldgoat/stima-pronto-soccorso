
from datetime import timedelta
import random
from src.simulator.generators.generator import Generator
import numpy as np


class TherapyTimeFromSampleGenerator(Generator):

    def __init__(self, therapy_times_for_esi):
        self.therapy_times = []
        self.therapy_times_occurrences = []
        for therapy_time_row in therapy_times_for_esi:
            self.therapy_times.append(therapy_time_row[0])
            self.therapy_times_occurrences.append(therapy_time_row[1])

    def generate_sample(self):
        return random.choices(self.therapy_times, weights=self.therapy_times_occurrences, k=1)[0]

    def generate_sample_with_minimum_value(self, minimum_value: timedelta):
        custom_therapy_times = []
        custom_therapy_times_occurrences = []
        for i in range(0, len(self.therapy_times)):
            if(self.therapy_times[i]>=minimum_value.seconds/60):
                custom_therapy_times.append(self.therapy_times[i])
                custom_therapy_times_occurrences.append(self.therapy_times_occurrences[i])
        return random.choices(custom_therapy_times, weights=custom_therapy_times_occurrences, k=1)[0]
