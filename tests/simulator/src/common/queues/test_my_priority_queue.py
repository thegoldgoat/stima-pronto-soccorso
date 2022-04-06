import unittest
from simulator.src.common.Queue.my_priority_queue import MyPriorityQueue

class TestMyPriorityQueue(unittest.TestCase):
    
    def setUp(self):
        
        self.x = MyPriorityQueue()
        self.y = MyPriorityQueue([6,9,3,6,5,3], True)
        self.z = MyPriorityQueue([21,23,421,43,33,0,6,523,1], True)
        
    def test_push(self):
        
        self.x.push(8)
        self.assertEqual(self.x.heap[0], 8)
        
        self.y.push(10)
        self.y.push(0)
        for k in range(0, len(self.y.heap)):
            if 2*k +1 < len(self.y.heap):
                self.assertGreaterEqual(self.y.heap[2*k + 1], self.y.heap[k])
            
            if 2*k +2 < len(self.y.heap):
                self.assertGreaterEqual(self.y.heap[2*k + 2], self.y.heap[k])

    def test_pop(self):
        
        with self.assertRaises(Exception):
            self.x.pop()
        
        self.assertEqual(self.y.pop(), 3)
        
        for k in range(0, len(self.y.heap)):
            if 2*k +1 < len(self.y.heap):
                self.assertGreaterEqual(self.y.heap[2*k + 1], self.y.heap[k])
            
            if 2*k +2 < len(self.y.heap):
                self.assertGreaterEqual(self.y.heap[2*k + 2], self.y.heap[k]) 
                
        self.assertEqual(self.z.pop(), 0)
        
        for k in range(0, len(self.z.heap)):
            if 2*k +1 < len(self.z.heap):
                self.assertGreaterEqual(self.z.heap[2*k + 1], self.z.heap[k])
            
            if 2*k +2 < len(self.z.heap):
                self.assertGreaterEqual(self.z.heap[2*k + 2], self.z.heap[k])

    def test_get_min(self):
            
        self.x = MyPriorityQueue([])
        with self.assertRaises(IndexError):
            self.x.get_min()
        
        self.assertEqual(self.y.get_min(), 3)
        self.assertEqual(self.z.get_min(), 0)
        

if __name__ == '__main__':
    unittest.main()