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
                link_url = re.match("<(.*)>; rel.*", link_url).groups()[0]
        return json.loads(response.text), link_url

    def collect(self, timeframe):
        url = "https://api.github.com/users/{0}/events".format(self.login)
        d = collections.defaultdict(list)

        # Paginate through the activity stream, mark first item in timeline
        # and last one to have a criteria for stopping pagination.
        while True:
            events_json, url = self._get_json(url)

            for event in events_json:
                created_at = rapport.util.datetime_from_iso8601(event["created_at"])
                if timeframe.contains(created_at):
                    d["events"].append(event)
                    if event["type"] == "CommitCommentEvent":
                        d["commit_comment_events"].append(event)
                    elif event["type"] == "CreateEvent":
                        d["create_events"].append(event)
                    elif event["type"] == "DeleteEvent":
                        d["delete_events"].append(event)
                    elif event["type"] == "ForkEvent":
                        d["fork_events"].append(event)
                    elif event["type"] == "GistEvent":
                        d["gist_events"].append(event)
                    elif event["type"] == "GollumEvent":
                        d["gollum_events"].append(event)
                    elif event["type"] == "IssuesEvent":
                        d["issues_events"].append(event)
                    elif event["type"] == "IssueCommentEvent":
                        d["issues_comment_events"].append(event)
                    elif event["type"] == "PullRequestEvent":
                        d["pull_request_events"].append(event)
                    elif event["type"] == "PullRequestReviewCommentEvent":
                        d["pull_request_review_comment_events"].append(event)
                    elif event["type"] == "PushEvent":
                        d["push_events"].append(event)
                    elif event["type"] == "TeamAddEvent":
                        d["team_add_events"].append(event)
                else:
                    if d["events"]:  # Found the last event inside the timeframe
                        url = None  # Don't fetch another page, got everything interesting
                        break  # No need to process the remaining events on this page

            if url is None:
                break  # Reached last page of activity stream, that's it :-)

        return self._results(d)


rapport.plugin.register("github", GithubPlugin)
