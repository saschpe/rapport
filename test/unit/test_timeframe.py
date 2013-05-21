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
        self.assertTrue(str(self.timeframe).startswith("Generic"))


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
        self.assertTrue(str(self.timeframe).startswith("Current week"))


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
        self.assertTrue(str(self.timeframe).startswith("Current month"))


class TestRecentDaysTimeframe(TimeframeTestCase):
    def setUp(self):
        super(TestRecentDaysTimeframe, self).setUp()
        self.timeframe = rapport.timeframe.RecentDaysTimeframe()

    def test_recent_days_timeframe(self):
        self.assertTrue(self.timeframe.contains(self.five_hours_ago))
        self.assertEqual(self.timeframe.start.hour, self.timeframe.end.hour)
        self.assertEqual(self.timeframe.start.minute,
                         self.timeframe.end.minute)
        self.assertEqual(self.timeframe.start.second,
                         self.timeframe.end.second)

    def test_last_seven_days_timeframe_str(self):
        self.assertTrue(str(self.timeframe).startswith("Recent days"))
