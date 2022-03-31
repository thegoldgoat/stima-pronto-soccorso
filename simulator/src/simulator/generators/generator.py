from abc import abstractmethod


class Generator():

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def generate_sample(self):
        pass
