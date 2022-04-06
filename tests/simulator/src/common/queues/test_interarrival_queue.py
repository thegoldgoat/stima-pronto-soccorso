from copy import deepcopy
import unittest
from simulator.src.common.Queue.interarrival_queue import InterarrivalQueue
from simulator.src.common.patient import Patient
from simulator.src.simulator.generators.gauss_generator import GaussGenerator
from simulator.src.simulator.generators.exponential_generator import ExponentialGenerator

class TestWaitingQueue(unittest.TestCase):
    
    def setUp(self):
        
        self.x = InterarrivalQueue()
    
    def test_reorder_samples(self):
        
        for i in range(0,3):
            for t in self.x.samples[i+1:]:
                self.x.samples[i][1] <= t[1]
    
    def test_peak(self):
        
        min = self.x.samples[0]
        for x in self.x.samples:
            if x[1] < min[1]:
                min = x    

        self.assertEqual(self.x.peak(), min)
    
    def test_pop_regenerate_decrement_others(self):
        
        y = InterarrivalQueue()
        y.samples = deepcopy(self.x.samples)
        return_value = self.x.pop_regenerate_decrement_others()
        self.assertEqual(y.samples[0], return_value)
        
        for t1 in self.x.samples:
            if t1[0] != return_value[0]:
                for t2 in y.samples:
                    if t2[0] == t1[0]:
                        self.assertEqual(t2[1] - return_value[1], t1[1])
        
        for i in range(0,3):
            for t in self.x.samples[i+1:]:
                self.x.samples[i][1] <= t[1]      
        
if __name__ == '__main__':
    unittest.main()