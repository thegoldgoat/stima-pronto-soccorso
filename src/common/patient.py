from src.simulator.generators.generator import Generator


class Patient():

    def __init__(self, id, therapy_generator: Generator, leave_generator: Generator, emergency_code, arrival_time):
        self.id = id
        self.therapy_generator = therapy_generator
        self.leave_generator = leave_generator
        self.emergency_code = emergency_code
        self.arrival_time = arrival_time
        self.leave_time = None
        self.therapy_time = None

    def generate_leave(self):
        self.leave_time = self.leave_generator.generate_sample()

    def generate_therapy(self):
        self.therapy_time = self.therapy_generator.generate_sample()

    def generate_all(self):
        self.generate_leave()
        self.generate_therapy()

    def decrement_leave_time(self,elapsed_time):
        self.leave_time -= elapsed_time    

    # Comparator 'less then' aka '<'
    def __lt__(self, nxt):
        if self.emergency_code < nxt.emergency_code:
            return True
        elif self.emergency_code > nxt.emergency_code:
            return False
        else:
            return self.arrival_time < nxt.arrival_time

    def clone_and_generate(self):
        return_value = Patient(self.id, self.therapy_generator, self.leave_generator,
                               self.emergency_code, self.arrival_time
                               )

        return_value.generate_all()

        return return_value
