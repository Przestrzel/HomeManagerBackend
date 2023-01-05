import pytest

from budget.models import Period
from utils.dates import DateService
import datetime


def test_every_setting_returns_two_elemental_list():
    date = datetime.date(2021, 1, 1)
    for period in Period:
        date_service = DateService(date, Period[period])
        assert len(date_service.get_range()) == 2, "Should be always two elements in list"


def test_get_week_range():
    date = datetime.date(2021, 1, 1)
    date_service = DateService(date, Period.WEEK)
    assert date_service.get_range() == [datetime.date(2020, 12, 28), datetime.date(2021, 1, 3)]


def test_get_month_range():
    date = datetime.date(2021, 1, 1)
    date_service = DateService(date, Period.MONTH)
    assert date_service.get_range() == [datetime.date(2021, 1, 1), datetime.date(2021, 1, 31)]


def test_get_year_range():
    date = datetime.date(2021, 1, 1)
    date_service = DateService(date, Period.YEAR)
    assert date_service.get_range() == [datetime.date(2021, 1, 1), datetime.date(2021, 12, 31)]


def test_get_range_raises_type_error():
    date = datetime.date(2021, 1, 1)
    date_service = DateService(date, 'DIFFERENT PERIOD')
    with pytest.raises(ValueError):
        date_service.get_range()
