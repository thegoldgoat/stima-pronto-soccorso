from datetime import datetime
from typing import List
from src.common.Rates.exponential_rate import ExponentialRate
from src.simulator.generators.exponential_generator import generate_exponential
from src.common.week_time import WeekTime, WEEKDAY_AMOUNT, HOURS_AMOUNT, MINUTES_AMOUNT


def get_hours_from_monday(target_datetime: datetime) -> WeekTime:
    return WeekTime(
        weekday=target_datetime.date().weekday(),
        hour=target_datetime.time().hour,
        minute=target_datetime.time().minute
    )


RATES_COUNT_IN_WEEK = 7 * 6


class ExponentialGeneratorTimeVariant():
    def __init__(self, rates: List[ExponentialRate]) -> None:
        if len(rates) != RATES_COUNT_IN_WEEK:
            raise Exception(
                "Exponential generator didn't get the correct amount of rates for the entire week")
        # Rates must be already ordered by day and hour_interval
        self.rates = rates
        pass

    def _find_index_interval(self, current_datetime: datetime):
        current_hours_from_monday = get_hours_from_monday(current_datetime)

        for index, rate in enumerate(self.rates):
            if rate.time_begin > current_hours_from_monday:
                return index - 1

        return len(self.rates) - 1

    def generate_sample(self, current_datetime: datetime):
        # Get the current rate index in the self.rates list
        rate_index = self._find_index_interval(current_datetime)
        return_sample_value = 0

        current_time_from_monday = get_hours_from_monday(current_datetime)

        while True:

            # Generate sample
            sample = generate_exponential(self.rates[rate_index].rate)

            updated_time_from_monday = current_time_from_monday.clone_and_increment(
                minutes=sample
            )

            if updated_time_from_monday.weekday != current_time_from_monday.weekday or \
                    updated_time_from_monday > self.rates[rate_index].time_end:
                # The sample overflowed the time interval assigned to this exponential rate
                # Update return_sample_value and redo sample considering new rate

                minutes_difference = self.rates[rate_index].time_end.difference(
                    current_time_from_monday)

                if minutes_difference < 0:
                    # A week overflow has occurred (e.g. current_time_from_monday = 23:50 at sunday and sample was 15 mins):
                    # Add a full week of minutes to this difference
                    minutes_difference += WEEKDAY_AMOUNT * HOURS_AMOUNT * MINUTES_AMOUNT

                return_sample_value += minutes_difference

                current_time_from_monday.increment(minutes=minutes_difference)

                rate_index = (rate_index + 1) % len(self.rates)
            else:
                # sample is OK
                return return_sample_value + sample
