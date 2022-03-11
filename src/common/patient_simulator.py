from src.common.patient import Patient


class PatientSimulator():

    def __init__(self, patient: Patient):
        # self.therapy_generator = patient.therapy_generator
        # self.leave_generator = patient.leave_generator

        self._therapy_time = patient.therapy_generator.generate_sample()
        self._leave_time = patient.leave_generator.generate_sample()

        # self.emergency_code = patient.emergency_code
        self.arrival_time = patient.arrival_time

    def update_therapy_time_and_check_if_finish(self, amount_passed):
        self._therapy_time -= amount_passed

        return self._therapy_time <= 0

    def update_leave_time_and_check_if_leave(self, amount_passed):
        self._leave_time -= amount_passed

        return self._leave_time <= 0
