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
