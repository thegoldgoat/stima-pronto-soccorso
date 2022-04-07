from src.common.patient import Patient


class TherapyPatient(Patient):

    def __init__(self, id, therapy_generator, therapy_time=None):
        super().__init__(id, therapy_generator, None, None, None)

        # If I received only the therapy_generator I generate instantly the therapy_time
        # The therapy time is generated instantly because the queue will order itself by TherapyPatient.therapy_time
        if therapy_time is None:
            self.generate_therapy()
        else:
            self.therapy_time = therapy_time

    def __lt__(self, nxt):
        return self.therapy_time < nxt.therapy_time

    def clone_and_generate(self):
        return_value = TherapyPatient(self.id, self.therapy_generator)

        return_value.generate_therapy()

        return return_value
