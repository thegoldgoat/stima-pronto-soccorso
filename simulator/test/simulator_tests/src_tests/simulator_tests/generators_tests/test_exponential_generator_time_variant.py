import unittest
from src.common.week_time import WeekTime
from src.common.Rates.exponential_rate import ExponentialRate
from src.simulator.generators.exponential_generator_time_variant import ExponentialGeneratorTimeVariant
from datetime import datetime


class TestExponentialGeneratorTimeVariant(unittest.TestCase):

    def create_rate_list(weekday: int):
        return [
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=3),
                            WeekTime(weekday=weekday, hour=7)),
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=7),
                            WeekTime(weekday=weekday, hour=11)),
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=11),
                            WeekTime(weekday=weekday, hour=15)),
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=15),
                            WeekTime(weekday=weekday, hour=19)),
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=19),
                            WeekTime(weekday=weekday, hour=23)),
            ExponentialRate(1,
                            WeekTime(weekday=weekday, hour=23),
                            WeekTime(weekday=weekday, hour=2))
        ]

    def setUp(self):
        self.rates = []
        for weekday in range(7):
            self.rates += TestExponentialGeneratorTimeVariant.create_rate_list(
                weekday)

    def check_index(self, target_datetime: datetime, expected_index: int):
        generator = ExponentialGeneratorTimeVariant(self.rates)
        self.assertEqual(
            expected_index, generator._find_index_interval(target_datetime))

    def test_first_interval(self):
        self.check_index(datetime(2022, 1, 3, 1), len(self.rates) - 1)

    def test_second_interval(self):
        self.check_index(datetime(2022, 1, 3, 3, 1), 0)

    def test_one_am_tuesday(self):
        self.check_index(datetime(2022, 1, 4, 1), 5)

    def test_three_am_tuesday(self):
        self.check_index(datetime(2022, 1, 4, 3), 6)

    def test_last_minus_one(self):
        self.check_index(datetime(2022, 1, 9, 22), len(self.rates) - 2)

    def test_last_interval(self):
        self.check_index(datetime(2022, 1, 9, 23), len(self.rates) - 1)
