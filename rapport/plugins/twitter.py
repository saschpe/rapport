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

"""
Twitter plugin.
"""

import tweepy

import rapport.plugin


class TwitterPlugin(rapport.plugin.Plugin):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, *args, **kwargs):
        super(TwitterPlugin, self).__init__(*args, **kwargs)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)

    def _get(self, timeline, timeframe):
        #TODO: Implement proper pagination instead of fixed count:
        count = 50
        statuses = []
        for status in timeline(count=count):
            if timeframe.contains(status.created_at):
                statuses.append(status)
        return statuses

    def collect(self, timeframe):
        mentions = self._get(self.api.mentions_timeline, timeframe)
        tweets = self._get(self.api.user_timeline, timeframe)
        retweets = self._get(self.api.retweets_of_me, timeframe)

        return self._results({"mentions": mentions,
                              "tweets": tweets,
                              "retweets": retweets})


rapport.plugin.register("twitter", TwitterPlugin)
