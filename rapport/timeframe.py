# Copyright 2013 Sascha Peilicke
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import datetime
import sys

import rapport.config


# http://stackoverflow.com/questions/304256/whats-the-best-way-to-find-the-inverse-of-datetime-isocalendar
def iso_year_start(iso_year):
    "The gregorian calendar date of the first day of the given ISO year"
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    "Gregorian calendar date for the given ISO year, week and day"
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)


def week_to_datetime(iso_year, iso_week):
    "datetime instance for the start of the given ISO year and week"
    gregorian = iso_to_gregorian(iso_year, iso_week, 0)
    return datetime.datetime.combine(gregorian, datetime.time(0))


class Timeframe(object):
    """Represents a period of time between a start and end time.

    :start: Start of timeframe (datetime object)
    :end: End of timeframe (datetime object)
    """
    def __init__(self, start, end):
        self._name = "Generic"
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def contains(self, date):
        """Checks if a date is within a timeframe.

        :date: The date to check
        """
        return self._start <= date and date < self._end

    def __str__(self):
        """Returns a string representation of a timeframe.
        """
        return "{0} [{1} - {2}]".format(self._name, self._start.isoformat(), self._end.isoformat())


class CurrentWeekTimeframe(Timeframe):
    """Current week timeframe (in UTC).
    """
    def __init__(self):
        self._name = "Current week"
        self._end = datetime.datetime.utcnow()
        # Compute the day but reset the hours/minutes/seconds to zero,
        # we want the exact week's start:
        week_start = self._end - datetime.timedelta(days=self._end.weekday())
        self._start = datetime.datetime(year=week_start.year,
                                        month=week_start.month,
                                        day=week_start.day)


class WeekTimeframe(Timeframe):
    """N-th week of year timeframe (in UTC).

    :week: Week number (starting from 1)
    """
    def __init__(self, week=1):
        self._name = "Week %d" % week
        now = datetime.datetime.utcnow()
        year = now.year
        self._start = week_to_datetime(year, week)
        if self._start > now:
            self._start = week_to_datetime(year - 1, week)
        self._end = self._start + datetime.timedelta(weeks=1)


class CurrentMonthTimeframe(Timeframe):
    """Current month timeframe (in UTC).
    """
    def __init__(self):
        self._name = "Current month"
        self._end = datetime.datetime.utcnow()
        self._start = datetime.datetime(year=self._end.year,
                                        month=self._end.month, day=1)


class MonthTimeframe(Timeframe):
    """N-th month of year timeframe (in UTC).

    :month: Month number (starting from 1)
    """
    def __init__(self, month=1):
        self._name = "Month"
        raise NotImplementedError()


class RecentDaysTimeframe(Timeframe):
    """Recent days timeframe (in UTC).
    """
    def __init__(self, days=14):
        self._name = "Recent days ({0})".format(days)
        self._end = datetime.datetime.utcnow()
        self._start = self._end - datetime.timedelta(days=days)
        self._days = days

_TIMEFRAME_CATALOG = {"current_month": CurrentMonthTimeframe,
                      "current_week": CurrentWeekTimeframe,
                      "month": MonthTimeframe,
                      "week": WeekTimeframe,
                      "recent_days": RecentDaysTimeframe}


def init(name, *args, **kwargs):
    """Instantiate a timeframe from the catalog.
    """
    if name in _TIMEFRAME_CATALOG:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print("Initialize timeframe {0}: {1} {2}".format(name, args, kwargs))
        try:
            return _TIMEFRAME_CATALOG[name](*args, **kwargs)
        except ValueError as e:
            print("Failed to initialize timeframe {0}: {1}!".format(name, e), file=sys.stderr)
    else:
        print("Failed to initialize timeframe {0}: Not in catalog!".format(name), file=sys.stderr)
        sys.exit(1)


def init_from_config():
    return init(rapport.config.get("timeframe", "default"))


def catalog():
    """Returns the list of registered timeframes.
    """
    return _TIMEFRAME_CATALOG.keys()
