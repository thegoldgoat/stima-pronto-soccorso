from src.common.week_time import WeekTime


class ExponentialRate():
    def __init__(self, rate: float, time_begin: WeekTime, time_end: WeekTime) -> None:
        self.rate = rate
        self.time_begin = time_begin
        self.time_end = time_end
