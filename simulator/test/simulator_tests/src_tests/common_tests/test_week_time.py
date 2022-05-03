import unittest
from src.common.week_time import WeekTime


class TestWeekTime(unittest.TestCase):

    def test_increment_normal(self):
        one = WeekTime()
        one.increment(1, 2, 3)
        self.assertEqual(1, one.weekday)
        self.assertEqual(2, one.hour)
        self.assertEqual(3, one.minute)

    def test_increment_overflow_minute(self):
        one = WeekTime(minute=58)
        one.increment(1, 2, 3)
        self.assertEqual(1, one.weekday)
        self.assertEqual(3, one.hour)
        self.assertEqual(1, one.minute)

    def test_increment_double_overflow_minute(self):
        one = WeekTime(minute=58)
        one.increment(1, 2, 63)
        self.assertEqual(1, one.weekday)
        self.assertEqual(4, one.hour)
        self.assertEqual(1, one.minute)

    def test_increment_triple_overflow_minute(self):
        one = WeekTime(minute=58)
        one.increment(1, 2, 63 + 24 * 60)
        self.assertEqual(2, one.weekday)
        self.assertEqual(4, one.hour)
        self.assertEqual(1, one.minute)

    def test_increment_overflow_hour(self):
        one = WeekTime(hour=12)
        one.increment(1, 13, 20)
        self.assertEqual(2, one.weekday)
        self.assertEqual(1, one.hour)
        self.assertEqual(20, one.minute)

    def test_increment_overflow_weekday(self):
        one = WeekTime(weekday=5, hour=12, minute=48)
        one.increment(2, 1, 1)
        self.assertEqual(0, one.weekday)
        self.assertEqual(13, one.hour)
        self.assertEqual(49, one.minute)

    def test_increment_overflow_weekday_hour_minute(self):
        one = WeekTime(weekday=5, hour=12, minute=48)
        one.increment(2, 11, 14)
        self.assertEqual(1, one.weekday)
        self.assertEqual(0, one.hour)
        self.assertEqual(2, one.minute)

    def test_comp_weekday(self):
        one = WeekTime(weekday=1, hour=10, minute=12)
        two = WeekTime(weekday=2, hour=8, minute=9)
        self.assertTrue(one < two)
        self.assertFalse(one > two)
        self.assertFalse(one == two)

    def test_comp_hour(self):
        one = WeekTime(weekday=1, hour=10, minute=12)
        two = WeekTime(weekday=1, hour=8, minute=9)
        self.assertTrue(one > two)
        self.assertFalse(one < two)
        self.assertFalse(one == two)

    def test_comp_minute(self):
        one = WeekTime(weekday=1, hour=8, minute=12)
        two = WeekTime(weekday=1, hour=8, minute=9)
        self.assertTrue(one > two)
        self.assertFalse(one < two)
        self.assertFalse(one == two)

    def test_comp_equal(self):
        one = WeekTime(weekday=1, hour=8, minute=12)
        two = WeekTime(weekday=1, hour=8, minute=12)
        self.assertFalse(one > two)
        self.assertFalse(one < two)
        self.assertTrue(one == two)


if __name__ == '__main__':
    unittest.main()
