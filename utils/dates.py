
from datetime import date as date_type, timedelta

from budget.models import Period


class DateService:

    def __init__(self, date: date_type, period: Period):
        self.date = date
        self.period = period

    def get_range(self) -> list[date_type]:
        if self.period == Period.WEEK:
            return self.get_week_range()
        elif self.period == Period.MONTH:
            return self.get_month_range()
        elif self.period == Period.YEAR:
            return self.get_year_range()

    def get_week_range(self) -> list[date_type]:
        day = self.date.weekday()
        start = self.date - timedelta(days=day)
        end = start + timedelta(days=6)
        return [start, end]

    def get_month_range(self) -> list[date_type]:
        return [self.date.replace(day=1), self.date.replace(day=31)]

    def get_year_range(self) -> list[date_type]:
        return [self.date.replace(month=1, day=1), self.date.replace(month=12, day=31)]


