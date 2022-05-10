from src.simulator.generators.generator import Generator
from numpy import random


def generate_exponential(rate):
    # return - round(math.log(random.random())/rate)
    return round(random.exponential(rate))


class ExponentialGenerator(Generator):

    def __init__(self, rate):
        self.rate = rate

    def generate_sample(self):
        return round(random.exponential(1 / self.rate))
