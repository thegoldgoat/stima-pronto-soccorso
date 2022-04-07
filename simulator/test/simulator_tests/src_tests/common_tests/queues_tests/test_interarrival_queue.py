from copy import deepcopy
import unittest
from src.common.Queue.interarrival_queue import InterarrivalQueue


class TestWaitingQueue(unittest.TestCase):

    def setUp(self):

        self.x = InterarrivalQueue()

    def test_reorder_samples(self):

        for i in range(0, 3):
            for t in self.x.samples[i+1:]:
                self.x.samples[i][1] <= t[1]

    def test_peek(self):

        min = self.x.samples[0]
        for x in self.x.samples:
            if x[1] < min[1]:
                min = x

        self.assertEqual(self.x.peek(), min)

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

        for i in range(0, 3):
            for t in self.x.samples[i+1:]:
                self.x.samples[i][1] <= t[1]

    def test_decrement_interarrive(self):

        temp = []
        for sample in self.x.samples:
            temp.append(sample[1])

        self.x.decrement_interarrive(1)

        index = 0
        for sample in self.x.samples:
            self.assertEqual(sample[1], temp[index] - 1)
            index += 1


if __name__ == '__main__':
    unittest.main()
