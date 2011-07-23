import json
import urllib
import urllib2


class API(object):
    """Accessor for the MunchyLunchy API."""

    @classmethod
    def verify_user(c, assertion):
        return request("auth/browserid", {"assertion": assertion}, "POST")

    @classmethod
    def verify_token(c, user):
        return request("auth/token", {}, "POST", user)

    @classmethod
    def taste_set(c, user, taste, likes=True):
        return request("tastes/set",
                       {"taste": taste,
                        "preference": "like" if likes else "dislike"},
                       "POST", user)

    @classmethod
    def taste_clear(c, user, taste):
        return request("tastes/clear", {"taste": taste}, "POST", user)

    @classmethod
    def taste_list(c, user):
        return request("tastes/list", user=user)

    @classmethod
    def taste_query(c, user, latitude, longitude):
        return request("tastes/query", {"lat": latitude, "lon": longitude},
                       "GET", user=user)

    @classmethod
    def health_ping(c):
        return request("health/ping", {})

    @classmethod
    def health_redis(c):
        return request("health/redis", {})

    @classmethod
    def places_decide(c, user, latitude, longitude):
        return request("places/decide", {"lat": latitude, "lon": longitude},
                       "GET", user=user)


class User(object):
    def __init__(self, email, token):
        self.email = email
        self.token = token


def request(path, params, method="GET", user=None):
    """Create a request to the MunchyLunchy API"""

    if user is not None:
        params["email"] = user.email
        params["token"] = user.token

    params = urllib.urlencode(params)
    host = "http://api.munchylunchy.com/v1/"

    try:
        if method == "GET":
            url = "%s%s?%s" % (host, path, params)
            request = urllib2.urlopen(url)
        else:
            url = "%s%s" % (host, path)
            request = urllib2.urlopen(url, params)

        response = request.read()
        if not response:
            return None
        return json.loads(response)
    except urllib2.HTTPError:
        return False

