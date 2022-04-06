import unittest
from simulator.src.common.Queue.waiting_queue import WaitingQueue
from simulator.src.common.patient import Patient
from simulator.src.simulator.generators.gauss_generator import GaussGenerator
from simulator.src.simulator.generators.exponential_generator import ExponentialGenerator

class TestWaitingQueue(unittest.TestCase):
    
    def setUp(self):
        
        self.x = WaitingQueue(3)
        self.patient1 = Patient('0000', GaussGenerator(1.5, 2), ExponentialGenerator(1.2), 1, 3600)
        self.patient2 = Patient('0001', GaussGenerator(2, 1), ExponentialGenerator(0.8), 1, 5000)
        self.patient3 = Patient('0002', GaussGenerator(1, 1.3), ExponentialGenerator(2), 2, 5000)
        self.patient4 = Patient('0003', GaussGenerator(3, 1), ExponentialGenerator(3), 4, 2000)
        self.patient5 = Patient('0004', GaussGenerator(1, 2), ExponentialGenerator(3), 0, 3000)
        
    def test_push(self):
        
        self.x.push(self.patient1)
        self.x.push(self.patient2)
        self.x.push(self.patient3)
        self.assertEqual(id(self.x.priority_queues[1].heap[0]), id(self.patient1))
        self.assertEqual(id(self.x.priority_queues[1].heap[1]), id(self.patient2))
        self.assertEqual(id(self.x.priority_queues[2].heap[0]), id(self.patient3))
        
        with self.assertRaises(IndexError):
            self.x.push(self.patient4)
    
    def test_pop(self):
        
        self.x.push(self.patient1)
        self.x.push(self.patient2)
        self.x.push(self.patient3)
        self.assertTrue(self.patient1, self.x.pop())
    
    def test_get_patients_count(self):
        
        self.x.push(self.patient1)
        self.x.push(self.patient2)
        self.x.push(self.patient3)
        self.assertEqual(self.x.get_patients_count(), 3)
        self.x.push(self.patient5)
        self.assertEqual(self.x.get_patients_count(), 4)
    
    def test_create_copy_and_generate(self):
        
        y = self.x.create_copy_and_generate()
        self.assertNotEqual(id(y), id(self.x))
        
        num_queue = 0
        i = 0
        for queue in self.x.priority_queues:
            for patient in queue.heap:
                self.assertEqual(patient.id, y.priority_queues[num_queue].heap[i].id)
                self.assertEqual(patient.emergency_code, y.priority_queues[num_queue].heap[i].emergency_code)
                self.assertEqual(patient.arrival_time, y.priority_queues[num_queue].heap[i].arrival_time)
                i += 1
            i = 0
            num_queue += 1
        
if __name__ == '__main__':
    unittest.main()