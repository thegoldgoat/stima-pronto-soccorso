import unittest
from simulator.src.common.therapy_patient import TherapyPatient
from simulator.src.simulator.generators.gauss_generator import GaussGenerator
from simulator.src.common.Queue.therapy_queue import TherapyQueue

class TestTherapyQueue(unittest.TestCase):

    def setUp(self):
        
        self.patient1 = TherapyPatient('0000', GaussGenerator(1, 1), 1000)
        self.patient2 = TherapyPatient('0001', GaussGenerator(2, 2), 500)
        self.patient3 = TherapyPatient('0002', GaussGenerator(1.5, 1), 200)
        self.patient4 = TherapyPatient('0003', GaussGenerator(3, 1.2), 145)
        
        self.x = TherapyQueue([ self.patient1, self.patient2, self.patient3], True)
    
    def test_therapy_queue_push(self):
        
        self.x.push(self.patient4)
        
        self.assertEqual(self.patient4, self.x.therapy_queue.get_min())
        
        for k in range(0, len(self.x.therapy_queue.heap)):
            if 2*k + 1 < len(self.x.therapy_queue.heap):
                self.assertTrue(self.x.therapy_queue.heap[k] < self.x.therapy_queue.heap[2*k + 1] or self.x.therapy_queue.heap[k].therapy_time == self.x.therapy_queue.heap[2*k + 1].therapy_time)
            
            if 2*k +2 < len(self.x.therapy_queue.heap):
                self.assertTrue(self.x.therapy_queue.heap[k] < self.x.therapy_queue.heap[2*k + 1] or self.x.therapy_queue.heap[k].therapy_time == self.x.therapy_queue.heap[2*k + 1].therapy_time)
    
    def test_create_copy_and_generate(self):
        
        y = self.x.create_copy_and_generate()
        self.assertNotEqual(id(y), id(self.x))
        i = 0
        for patient in self.x.therapy_queue.heap:
            self.assertEqual(patient.id, y.therapy_queue.heap[i].id)
            i += 1
        
        for k in range(0, len(y.therapy_queue.heap)):
            if 2*k + 1 < len(y.therapy_queue.heap):
                self.assertTrue(y.therapy_queue.heap[k] < y.therapy_queue.heap[2*k + 1] or y.therapy_queue.heap[k].therapy_time == y.therapy_queue.heap[2*k + 1].therapy_time)
            
            if 2*k +2 < len(y.therapy_queue.heap):
                self.assertTrue(y.therapy_queue.heap[k] < y.therapy_queue.heap[2*k + 1] or y.therapy_queue.heap[k].therapy_time == y.therapy_queue.heap[2*k + 1].therapy_time)    
        

if __name__ == "__main__":
    unittest.main()