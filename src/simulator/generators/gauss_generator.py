from .generator import Generator
import numpy as np


class GaussGenerator(Generator):

    def __init__(self, average, variance):
        self.average = average
        self.variance = variance

    def generate_sample(self):
        # TODO: to implement
        return max(0, np.random.default_rng().normal(self.average, self.variance)) # value can't be less than zero
