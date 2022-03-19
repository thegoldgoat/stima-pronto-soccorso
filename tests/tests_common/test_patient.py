import unittest
from src.common.patient import Patient
from src.simulator.generators.gauss_generator import GaussGenerator
from src.simulator.generators.exponential_generator import ExponentialGenerator

class TestPatient(unittest.TestCase):
    
    def setUp(self):
        self.patient1 = Patient('0000', GaussGenerator(1, 1), ExponentialGenerator(0.5), 2, 3600)
        self.patient2 = Patient('0001', GaussGenerator(2, 2), ExponentialGenerator(3), 1, 10800)
        self.patient3 = Patient('0002', GaussGenerator(1.5, 1), ExponentialGenerator(2), 2, 9000)
        self.patient1.generate_all()
        self.patient2.generate_all()
        self.patient3.generate_all()
        
    def test_it(self):
        
        self.assertFalse(self.patient1.__lt__(self.patient2))
        self.assertTrue(self.patient2.__lt__(self.patient3))
        
        if self.patient1.arrival_time < self.patient3.arrival_time:
            self.assertTrue(self.patient1.__lt__(self.patient3))
        else:
            self.assertFalse(self.patient1.__lt__(self.patient3))
        
    def test_clone_and_generate(self):
        
        patient4 = self.patient1.clone_and_generate()
        self.assertNotEqual(id(patient4), id(self.patient1))
        self.assertTrue(isinstance(patient4, Patient))
        self.assertEqual(patient4.id, self.patient1.id)
        self.assertEqual(patient4.emergency_code, self.patient1.emergency_code)
        self.assertEqual(patient4.arrival_time, self.patient1.arrival_time)
    
if __name__ == '__main__':
    unittest.main()