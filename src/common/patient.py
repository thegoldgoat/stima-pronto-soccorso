class Patient():

    def __init__(self, therapy_generator, leave_generator, emergency_code, arrival_time):
        self.therapy_generator = therapy_generator
        self.leave_generator = leave_generator
        self.emergency_code = emergency_code
        self.arrival_time = arrival_time

    def generate_leave(self):
        self.leave_time = self.leave_generator.generate()

    def generate_therapy(self):
        self.therapy_time = self.therapy_generator.generate()

    def generate_all(self):
        self.generate_leave()
        self.generate_therapy()
