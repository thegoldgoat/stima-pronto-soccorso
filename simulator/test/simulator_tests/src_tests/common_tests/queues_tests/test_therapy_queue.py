import unittest
from src.common.therapy_patient import TherapyPatient
from src.simulator.generators.gauss_generator import GaussGenerator
from src.common.Queue.therapy_queue import TherapyQueue


class TestTherapyQueue(unittest.TestCase):

    def setUp(self):

        self.patient1 = TherapyPatient('0000', GaussGenerator(1, 1), 1000)
        self.patient2 = TherapyPatient('0001', GaussGenerator(2, 2), 500)
        self.patient3 = TherapyPatient('0002', GaussGenerator(1.5, 1), 200)
        self.patient4 = TherapyPatient('0003', GaussGenerator(3, 1.2), 145)

        self.x = TherapyQueue(3)

    def test_push_is_full(self):

        self.x.push(self.patient4)
        self.x.push(self.patient2)
        self.x.push(self.patient3)

        self.assertTrue(self.x.is_full())

        with self.assertRaises(Exception):
            self.x.push(self.patient1)

        self.assertEqual(self.patient4, self.x.therapy_queue.get_min())

    def test_peek(self):

        self.x.push(self.patient4)
        self.x.push(self.patient2)
        self.x.push(self.patient3)
        self.assertEqual(self.x.peek(), self.patient4)

    def test_pop(self):

        self.x.push(self.patient1)
        self.x.push(self.patient2)
        self.x.push(self.patient3)
        self.assertEqual(self.patient3, self.x.pop())

    def test_decrement_therapy_times(self):

        self.x.push(self.patient4)
        self.x.push(self.patient2)
        self.x.push(self.patient3)

        self.x.decrement_therapy_times(100)

        self.assertEqual(self.patient2.therapy_time, 400)
        self.assertEqual(self.patient3.therapy_time, 100)
        self.assertEqual(self.patient4.therapy_time, 45)


if __name__ == "__main__":
    unittest.main()
