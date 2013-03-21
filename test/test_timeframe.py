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
import unittest

import rapport.timeframe


class TimeframeTestCase(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.a_day_ago = self.now - datetime.timedelta(days=1)
        self.five_hours_ago = self.now - datetime.timedelta(hours=5)


class TestTimeframe(TimeframeTestCase):
    def setUp(self):
        super(TestTimeframe, self).setUp()
        self.timeframe = rapport.timeframe.Timeframe(start=self.a_day_ago,
                                                     end=self.now)

    def test_timeframe(self):
        self.assertEqual(self.a_day_ago, self.timeframe.start)
        self.assertEqual(self.now, self.timeframe.end)
        self.assertTrue(self.timeframe.contains(self.five_hours_ago))

    def test_timeframe_str(self):
        self.assertEqual("timeframe", str(self.timeframe))


class TestCurrentWeekTimeframe(TimeframeTestCase):
    def setUp(self):
        super(TestCurrentWeekTimeframe, self).setUp()
        self.timeframe = rapport.timeframe.CurrentWeekTimeframe()

    def test_current_week_timeframe(self):
        start = self.timeframe.start
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)
        self.assertEqual(start.second, 0)
        self.assertTrue(self.timeframe.contains(self.five_hours_ago))

    def test_current_week_timeframe_str(self):
        self.assertEqual("current_week", str(self.timeframe))


class TestCurrentMonthTimeframe(TimeframeTestCase):
    def setUp(self):
        super(TestCurrentMonthTimeframe, self).setUp()
        self.timeframe = rapport.timeframe.CurrentMonthTimeframe()

    def test_current_week_timeframe(self):
        start = self.timeframe.start
        self.assertEqual(start.hour, 0)
        self.assertEqual(start.minute, 0)
        self.assertEqual(start.second, 0)
        self.assertTrue(self.timeframe.contains(self.five_hours_ago))

    def test_current_week_timeframe_str(self):
        self.assertEqual("current_month", str(self.timeframe))


class TestNLastDaysTimeframe(TimeframeTestCase):
    def setUp(self):
        super(TestNLastDaysTimeframe, self).setUp()
        self.timeframe = rapport.timeframe.NLastDaysTimeframe()

    def test_n_last_days_timeframe(self):
        self.assertTrue(self.timeframe.contains(self.five_hours_ago))
        self.assertEqual(self.timeframe.start.hour, self.timeframe.end.hour)
        self.assertEqual(self.timeframe.start.minute,
                         self.timeframe.end.minute)
        self.assertEqual(self.timeframe.start.second,
                         self.timeframe.end.second)

    def test_last_seven_days_timeframe_str(self):
        self.assertEqual("n_last_days", str(self.timeframe))
