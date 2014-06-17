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
Github plugin.
"""

import collections
import json
import re

import requests

import rapport.plugin
import rapport.util


class GithubPlugin(rapport.plugin.Plugin):
    def __init__(self, *args, **kwargs):
        super(GithubPlugin, self).__init__(*args, **kwargs)
        #TODO: Maybe rather use oauth?

    def _get_json(self, url):
        response = requests.get(url, auth=(self.login, self.password))
        link_url = None
        if "link" in response.headers:
            link_url = response.headers["link"]
            if link_url.startswith("<"):
                # If URL looks like this: '<https://api.github.com/user/$ID/events?page=2>; rel="next"'
                m = re.match('<([^>]+)>; rel="next"', link_url)
                if m:
                    link_url = m.groups()[0]
                # otherwise it's probably a rel="prev" link which we don't want
        return json.loads(response.text), link_url

    def collect(self, timeframe):
        url = "https://api.github.com/users/{0}/events".format(self.login)
        d = {
            "events_by_time" : [],
            "events_by_type" : collections.defaultdict(list),
            "events_by_repo" : {},
        }

        # Paginate through the activity stream, mark first item in timeline
        # and last one to have a criteria for stopping pagination.
        while True:
            events_json, url = self._get_json(url)
            if 'message' in events_json:
                msg = events_json['message']
                if 'documentation_url' in events_json:
                    msg += ' (%s)' % events_json['documentation_url']
                raise RuntimeError(msg)

            for event in events_json:
                created_at = rapport.util.datetime_from_iso8601(event["created_at"])
                if timeframe.contains(created_at):
                    d["events_by_time"].append(event)
                    d["events_by_type"][event["type"]].append(event)

                    repo = event["repo"]["name"]
                    if repo not in d["events_by_repo"]:
                        d["events_by_repo"][repo] = collections.defaultdict(list)
                    d["events_by_repo"][repo]["events"].append(event)
                    d["events_by_repo"][repo][event["type"]].append(event)
                    #import code; code.interact(local=locals())
                else:
                    if d["events_by_time"]:  # Found the last event inside the timeframe
                        url = None  # Don't fetch another page, got everything interesting
                        break  # No need to process the remaining events on this page

            if url is None:
                break  # Reached last page of activity stream, that's it :-)

        return self._results(d)


rapport.plugin.register("github", GithubPlugin)
