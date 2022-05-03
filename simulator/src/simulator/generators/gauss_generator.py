from src.simulator.generators.generator import Generator
from random import normalvariate


class GaussGenerator(Generator):

    def __init__(self, average, variance):
        self.average = average
        self.variance = variance

    def generate_sample(self):
        sample = -1

        while sample < 0:
            sample = normalvariate(self.average, self.variance)

        return round(sample)
