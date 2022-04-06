import unittest
from simulator.src.common.therapy_patient import TherapyPatient
from simulator.src.simulator.generators.gauss_generator import GaussGenerator


class TestTherapyPatient(unittest.TestCase):
    
    def setUp(self):
        
        self.patient1 = TherapyPatient('0000', GaussGenerator(1, 1), 1000)
        self.patient2 = TherapyPatient('0001', GaussGenerator(2, 2), 500)
        self.patient3 = TherapyPatient('0002', GaussGenerator(1.5, 1))
        
    def test_it(self):
        
        self.assertFalse(self.patient1.__lt__(self.patient2))
        
        if self.patient1.therapy_time < self.patient3.therapy_time:
            self.assertTrue(self.patient1.__lt__(self.patient3))
        else:
            self.assertFalse(self.patient1.__lt__(self.patient3))
        
    def test_clone_and_generate(self):
        
        patient4 = self.patient1.clone_and_generate()
        self.assertNotEqual(id(patient4), id(self.patient1))
        self.assertTrue(isinstance(patient4, TherapyPatient))
        self.assertEqual(patient4.id, self.patient1.id)
        self.assertIsNotNone(patient4.therapy_time)
        
    
if __name__ == '__main__':
    unittest.main()