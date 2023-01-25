from dataclasses import dataclass
from datetime import date


@dataclass(order=True)  # for date1 < date2
class Date:
    year: int
    month: int
    day: int

    def __post_init__(self):
        init_date = f'year: {self.year}, month: {self.month}, day: {self.day}'
        try:
            self.year = int(self.year)
            self.month = int(self.month)
            self.day = int(self.day)
            date(self.year, self.month, self.day)
        except (ValueError, TypeError):
            raise ValueError(f'Check the date - {init_date}')

    def swap(self, other):
        year, month, day = other.year, other.month, other.day
        other.year, other.month, other.day = self.year, self.month, self.day
        self.year, self.month, self.day = year, month, day
        return self


@dataclass
class DateRange:
    start: Date
    end: Date

    def __post_init__(self):
        if self.start > self.end:
            self.start.swap(self.end)

    # for list.sort(), sorted() & daterange1 < daterange2
    def __lt__(self, other):
        return self.start < other.start

    def intersects(self, other):
        if self.end < other.start or other.end < self.start:
            return False
        return True

    #  call a check intersects() before call merge() if necessary
    def merge(self, other):
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)
        return self


def get_ranges_wo_insurance(insurance_periods: list[DateRange]) -> list[DateRange]:
    slices = sorted(insurance_periods[:])
    i = 0
    while i <= len(slices)-2:
        if slices[i].intersects(slices[i+1]):
            slices[i].merge(slices[i+1])
            slices.pop(i+1)
            continue
        i += 1
    return [DateRange(slices[i].end, slices[i+1].start)
            for i in range(len(slices) - 1)]


if __name__ == '__main__':

    _insurances = [
        DateRange(Date(2020, 1, 1), Date(2020, 6, 25)),
        DateRange(Date(2020, 7, 1), Date(2020, 8, 31)),
        DateRange(Date(2020, 6, 29), Date(2020, 7, 31)),
        DateRange(Date(2020, 10, 1), Date(2020, 12, 31)),
    ]

    assert get_ranges_wo_insurance(_insurances) == [
        DateRange(Date(2020, 6, 25), Date(2020, 6, 29)),
        DateRange(Date(2020, 8, 31), Date(2020, 10, 1)),
    ]

    assert get_ranges_wo_insurance([]) == []

    _insurances = [
        DateRange(Date(2020, 1, 1), Date(2020, 7, 15)),
        DateRange(Date(2020, 7, 1), Date(2020, 12, 31)),
    ]
    assert get_ranges_wo_insurance(_insurances) == []
