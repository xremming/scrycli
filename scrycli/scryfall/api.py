import time
import sys

import requests

from ..__init__ import __version__
from .card import ScryfallCard


class Scryfall:

    class APIError(Exception):
        pass

    class TooManyRequests(Exception):
        pass

    API_URL = "https://api.scryfall.com"
    USER_AGENT = (
        "scrycli/{} (github.com/polarpayne/scrycli) "
        "requests/{} "
        "python/{}.{}.{}"
    ).format(
        __version__,
        requests.__version__,
        sys.version_info.major,
        sys.version_info.minor,
        sys.version_info.micro
    )
    SLEEP = 0.1

    def __init__(self, isatty=False, urls=False):
        self.card_kwargs = {
            "isatty": isatty,
            "urls": urls
        }

        self._r = requests.session()
        self._r.headers.update({
            "User-Agent": self.USER_AGENT
        })

    def _check(self, response):
        if response.status_code == 200:
            data = response.json()
            return data
        elif response.status_code == 429:
            raise self.TooManyRequests("too many requests")
        elif 400 <= response.status_code <= 599:
            data = response.json()
            for i in data.get("warnings", []):
                print(i, file=sys.stderr)
            print(data["details"], file=sys.stderr)
            raise self.APIError("API returned status code " + str(response.status_code))
        else:
            raise APIError("Unknown error (status code: " + str(response.status_code))

    def _get_url(self, url, params=None):
        if params is None:
            params = {}

        return self._check(
            self._r.get(url, params=params)
        )

    def _get(self, api, params=None):
        if params is None:
            params = {}

        return self._check(
            self._r.get(self.API_URL + api, params=params)
        )

    def search(self, q, order):
        data = self._get("/cards/search", params={"q": q, "order": order})

        yield from (ScryfallCard(card, **self.card_kwargs) for card in data["data"])

        more = data.get("has_more", False)
        next_page = data.get("next_page", None)
        while more and next_page:
            time.sleep(self.SLEEP)
            data = self._get_url(next_page)
            more = data.get("has_more", False)
            next_page = data.get("next_page", None)
            yield from (ScryfallCard(card, **self.card_kwargs) for card in data["data"])

    def named(self, name, exact=False):
        params = {"fuzzy": name}
        if exact:
            params = {"exact": name}

        return ScryfallCard(self._get("/cards/named", params=params), **self.card_kwargs)

    def random(self, count=1):
        for _ in range(count):
            yield ScryfallCard(self._get("/cards/random"), **self.card_kwargs)
            time.sleep(self.SLEEP)

    def catalog(self, what):
        return self._get("/catalog/" + what)["data"]
