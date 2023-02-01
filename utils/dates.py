import datetime
from budget.models import Period


class DateService:
    def __init__(self, date: datetime.date, period: Period):
        self.date = date
        self.period = period

    def get_range(self) -> list[datetime.date]:
        if self.period == Period.WEEK:
            return self.get_week_range()
        elif self.period == Period.MONTH:
            return self.get_month_range()
        elif self.period == Period.YEAR:
            return self.get_year_range()
        raise ValueError(f'Period "{self.period}" not supported')

    def get_week_range(self) -> list[datetime.date]:
        day = self.date.weekday()
        start = self.date - datetime.timedelta(days=day)
        end = start + datetime.timedelta(days=6)
        return [start, end]

    def get_month_range(self) -> list[datetime.date]:
        return [self.date.replace(day=1), self.date.replace(day=31)]

    def get_year_range(self) -> list[datetime.date]:
        return [self.date.replace(month=1, day=1), self.date.replace(month=12, day=31)]
