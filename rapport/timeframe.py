# Copyright (c) 2013, Sascha Peilicke <saschpe@gmx.de>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program (see the file COPYING); if not, write to the
# Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA

import datetime

import rapport.config
import rapport.util


class Timeframe(object):
    """Represents a period of time between a start and end time.

    :start: Start of timeframe (datetime object)
    :end: End of timeframe (datetime object)
    """
    def __init__(self, start, end):
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
        """Returns the class name in underscores.

        Additionally, for sub-classes, the suffix '_timeframe' is split off.

            >>> from rapport import timeframe
            >>> t = timeframe.Timeframe(start=None, end=None)
            >>> str(t)
            'timeframe'
        """
        return rapport.util.camelcase_to_underscores(self.__class__.__name__).rsplit("_timeframe")[0]


class CurrentWeekTimeframe(Timeframe):
    """Current week timeframe (in UTC).
    """
    def __init__(self):
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
        raise NotImplementedError()


class CurrentMonthTimeframe(Timeframe):
    """Current month timeframe (in UTC).
    """
    def __init__(self):
        self._end = datetime.datetime.utcnow()
        self._start = datetime.datetime(year=self._end.year,
                                        month=self._end.month, day=1)


class MonthTimeframe(Timeframe):
    """N-th month of year timeframe (in UTC).

    :month: Month number (starting from 1)
    """
    def __init__(self, month=1):
        raise NotImplementedError()


class NLastDaysTimeframe(Timeframe):
    """'N' last days timeframe (in UTC).
    """
    def __init__(self, days=7):
        self._end = datetime.datetime.utcnow()
        self._start = self._end - datetime.timedelta(days=days)


_TIMEFRAME_CATALOG = {"current_month": CurrentMonthTimeframe,
                      "current_week": CurrentWeekTimeframe,
                      "month": MonthTimeframe,
                      "week": WeekTimeframe,
                      "n_last_days": NLastDaysTimeframe}


def init(name, *args, **kwargs):
    """Instantiate a timeframe from the catalog.
    """
    if name in _TIMEFRAME_CATALOG:
        if rapport.config.get_int("rapport", "verbosity") >= 2:
            print "Initialize timeframe {0}: {1} {2}".format(name, args, kwargs)
        try:
            return _TIMEFRAME_CATALOG[name](*args, **kwargs)
        except ValueError as e:
            print >>sys.stderr, "Failed to initialize timeframe {0}: {1}!".format(name, e)
    else:
        print >>sys.stderr, "Failed to initialize timeframe {0}: Not in catalog!".format(name)


def init_from_config():
    return init(rapport.config.get("timeframe", "default"))


def catalog():
    """Returns the list of registered timeframes.
    """
    return _TIMEFRAME_CATALOG.keys()
