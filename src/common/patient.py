class Patient():

    def __init__(self, therapy_generator, leave_generator, emergency_code, arrival_time):
        self.therapy_generator = therapy_generator
        self.leave_generator = leave_generator
        self.emergency_code = emergency_code
        self.arrival_time = arrival_time
