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

from rapport.util import camelcase_to_underscores


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

            >>> t = Timeframe()
            >>> str(t)
            'timeframe'
        """
        return camelcase_to_underscores(self.__class__.__name__) \
            .rsplit("_timeframe")[0]


class CurrentWeekTimeframe(Timeframe):
    def __init__(self):
        self._end = datetime.datetime.utcnow()
        # Compute the day but reset the hours/minutes/seconds to zero,
        # we want the exact week's start:
        week_start = self._end - datetime.timedelta(days=self._end.weekday())
        self._start = datetime.datetime(year=week_start.year,
                                        month=week_start.month,
                                        day=week_start.day)


class CurrentMonthTimeframe(Timeframe):
    def __init__(self):
        self._end = datetime.datetime.utcnow()
        self._start = datetime.datetime(year=self._end.year,
                                        month=self._end.month, day=1)


class NLastDaysTimeframe(Timeframe):
    """
    """
    def __init__(self, days=7):
        self._end = datetime.datetime.utcnow()
        self._start = self._end - datetime.timedelta(days=days)
