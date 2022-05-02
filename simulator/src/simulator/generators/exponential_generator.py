from src.simulator.generators.generator import Generator
import numpy as np
from math import ceil


def generate_exponential(rate):
    return ceil(np.random.default_rng().exponential(rate))


class ExponentialGenerator(Generator):

    def __init__(self, rate):
        self.rate = rate

    # TODO: Implement ourselves (?)
    def generate_sample(self):
        return ceil(np.random.default_rng().exponential(self.rate))
