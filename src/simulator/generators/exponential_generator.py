from .generator import Generator
import numpy as np


class ExponentialGenerator(Generator):

    def __init__(self, rate):
        self.rate = rate

    # TODO: Implement ourselves (?)
    def generate_sample(self):
        return np.random.default_rng().exponential(self.rate)
