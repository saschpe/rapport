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
    def test_timeframe(self):
        timeframe = rapport.timeframe.Timeframe(start=self.a_day_ago, end=self.now)

        self.assertEqual(self.a_day_ago, timeframe.start)
        self.assertEqual(self.now, timeframe.end)
        self.assertTrue(timeframe.contains(self.five_hours_ago))
        self.assertEqual("timeframe", str(timeframe))


class TestCurrentWeekTimeframe(TimeframeTestCase):
    def test_current_week_timeframe(self):
        timeframe = rapport.timeframe.CurrentWeekTimeframe()
 
        self.assertTrue(timeframe.contains(self.five_hours_ago))
        self.assertEqual("current_week", str(timeframe))
