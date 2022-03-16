from src.common.patient import Patient

class TherapyPatient():

    def __init__(self,id, therapy_generator, therapy_time = None):
        self.id = id
        self.therapy_generator = therapy_generator

        # If therapy time has been generated before (for example in a Patient) I save it
        self.therapy_time = therapy_time 
        
        # If I received only the therapy_generator I generate instantly the therapy_time 
        # The therapy time is generated instantly because the queue will order itself by TherapyPatient.therapy_time
        if self.therapy_time is None:
            self.generate_therapy()
        

    def generate_therapy(self):
        """ Generate the therapy time using the therapy generator """
        self.therapy_time = self.therapy_generator.generate_sample()

    def __lt__(self, nxt):
        if self.therapy_time < nxt.therapy_time:
            return True
        else:
            return False

    @staticmethod
    def init_with_patient(patient: Patient):
        """ Get a new TherapyPatient using Patient data """
        return TherapyPatient(patient.id,patient.therapy_generator,patient.therapy_time)