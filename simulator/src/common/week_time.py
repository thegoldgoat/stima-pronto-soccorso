WEEKDAY_AMOUNT = 7
HOURS_AMOUNT = 24
MINUTES_AMOUNT = 60


class WeekTime():
    def __init__(self, weekday: int = 0, hour: int = 0, minute: int = 0) -> None:
        if weekday >= WEEKDAY_AMOUNT:
            raise Exception("{} is a too high number for a weekday, which should be {} at max".format(
                weekday, WEEKDAY_AMOUNT))

        if hour >= HOURS_AMOUNT:
            raise Exception("{} is a too high number for an hour, which should be {} at max".format(
                hour, HOURS_AMOUNT))

        if minute >= MINUTES_AMOUNT:
            raise Exception("{} is a too high number for a minute, which should be {} at max".format(
                minute, MINUTES_AMOUNT))

        self.weekday = weekday
        self.hour = hour
        self.minute = minute

    def __lt__(self, other) -> bool:
        if self.weekday < other.weekday:
            return True

        if self.weekday > other.weekday:
            return False

        if self.hour < other.hour:
            return True

        if self.hour > other.hour:
            return False

        return self.minute < other.minute

    def __gt__(self, other) -> bool:
        return self != other and other < self

    def __eq__(self, other) -> bool:
        return self.weekday == other.weekday and self.hour == other.hour and self.minute == other.minute

    def increment(self, days=0, hours=0, minutes=0) -> None:
        self.minute += minutes

        self.hour += self.minute // MINUTES_AMOUNT
        self.minute %= MINUTES_AMOUNT

        self.hour += hours

        self.weekday += self.hour // HOURS_AMOUNT
        self.hour %= HOURS_AMOUNT

        self.weekday += days
        self.weekday %= WEEKDAY_AMOUNT

    def clone_and_increment(self, days=0, hours=0, minutes=0):
        cloned = self.clone()
        cloned.increment(days, hours, minutes)
        return cloned

    def clone(self):
        return WeekTime(self.weekday, self.hour, self.minute)

    def calculate_total_minutes(self):
        return self.minute + (self.hour + self.weekday * HOURS_AMOUNT) * MINUTES_AMOUNT

    def difference(self, other):
        self_minutes = self.calculate_total_minutes()
        other_minutes = other.calculate_total_minutes()

        return self_minutes - other_minutes
