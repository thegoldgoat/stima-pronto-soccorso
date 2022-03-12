from .generator import Generator


class GaussGenerator(Generator):

    def __init__(self, average, variance):
        self.average = average
        self.variance = variance

    def generate_sample(self):
        # TODO: to implement
        return 12345
