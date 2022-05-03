from src.simulator.generators.generator import Generator
from random import expovariate


def generate_exponential(rate):
    # return - round(math.log(random.random())/rate)
    return round(expovariate(rate))


class ExponentialGenerator(Generator):

    def __init__(self, rate):
        self.rate = rate

    def generate_sample(self):
        return round(expovariate(1 / self.rate))
