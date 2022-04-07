from src.simulator.generators.generator import Generator
import numpy as np
from math import floor


class GaussGenerator(Generator):

    def __init__(self, average, variance):
        self.average = average
        self.variance = variance

    def generate_sample(self):
        # TODO: to implement
        # value can't be less than zero
        return floor(max(1, np.random.default_rng().normal(self.average, self.variance)))
