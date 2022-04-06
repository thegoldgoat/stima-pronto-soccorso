import unittest
from simulator.src.common.patient import Patient
from simulator.src.simulator.generators.gauss_generator import GaussGenerator
from simulator.src.simulator.generators.exponential_generator import ExponentialGenerator

class TestPatient(unittest.TestCase):
    
    def setUp(self):
        
        self.patient1 = Patient('0000', GaussGenerator(1, 1), ExponentialGenerator(0.5), 2, 3600)
        self.patient2 = Patient('0001', GaussGenerator(2, 2), ExponentialGenerator(3), 1, 10800)
        self.patient3 = Patient('0002', GaussGenerator(1.5, 1), ExponentialGenerator(2), 2, 9000)
    
    def test_generate_leave(self):
        
        self.patient1.generate_leave()
        self.assertIsNotNone(self.patient1.leave_time)
        
    def test_generate_therapy(self):
        
        self.patient1.generate_therapy()
        self.assertIsNotNone(self.patient1.therapy_time)
        
    def test_generate_all(self):
        
        self.patient1.generate_all()
        self.assertIsNotNone(self.patient1.leave_time)
        self.assertIsNotNone(self.patient1.leave_time)
        
    def test_decrement_leave_time(self):
        
        self.patient1.generate_leave()
        temp = self.patient1.leave_time;
        self.patient1.decrement_leave_time(1)
        self.assertEqual(self.patient1.leave_time, temp - 1)
        
    def test_decrement_therapy_time(self):
        
        self.patient1.generate_therapy()
        temp = self.patient1.therapy_time;
        self.patient1.decrement_therapy_time(1)
        self.assertEqual(self.patient1.therapy_time, temp - 1)
     
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