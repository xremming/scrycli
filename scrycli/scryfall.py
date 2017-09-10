from pprint import pprint
import json
import time
import sys

import requests

from .__init__ import __version__


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

    def __init__(self, isatty=False):
        self.card_kwargs = {
            "isatty": isatty
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
        else:
            raise self.APIError("API returned status code " + response.status_code)

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

    def random(self, count=1):
        for _ in range(count):
            yield ScryfallCard(self._get("/cards/random", **self.card_kwargs))
            time.sleep(self.SLEEP)


class ScryfallCard:

    LONGEST_MANA_COST = len("{W}{W}{U}{U}{B}{B}{R}{R}{G}{G}")
    LONGEST_NAME = len("Our Market Research Shows That Players Like Really Long Card Names So We Made this Card to Have the Absolute Longest Card Name Ever Elemental")
    LONGEST_TYPE_LINE = len("Legendary Enchantment Creature — God")

    class CardFace:

        def __init__(self, data, isatty=False):
            self.isatty = isatty

            self.name = data["name"]
            self.mana_cost = data.get("mana_cost", None)
            self.type_line = data["type_line"]
            self.oracle_text = data.get("oracle_text", None)
            self.power = data.get("power", None)
            self.toughness = data.get("toughness", None)

        def __str__(self):
            out = []
            out.append(self.name)
            if self.mana_cost:
                out[0] += " " + self.mana_cost
            out.append(bold(self.type_line, self.isatty))
            if self.oracle_text:
                out.append(self.oracle_text)
            if self.power and self.toughness:
                out.append(self.power + "/" + self.toughness)

            return "\n".join(out)

    def __init__(self, data, isatty=False):
        self.isatty = isatty

        self._data = data
        self.name = data["name"]
        self.mana_cost = data["mana_cost"]
        self.type_line = data.get("type_line", None)
        self.oracle_text = data.get("oracle_text", None)
        self.flavor_text = data.get("flavor_text", None)
        self.power = data.get("power", None)
        self.toughness = data.get("toughness", None)

        self.card_faces = []
        for face in data.get("card_faces", []):
            self.card_faces.append(self.CardFace(face, isatty=isatty))

    def __str__(self):
        if len(self.card_faces) > 0:
            return "\n***\n".join(map(str, self.card_faces))

        out = []
        out.append(self.name)
        if self.mana_cost:
            out[0] += " " + self.mana_cost
        if self.type_line:
            out.append(bold(self.type_line, self.isatty))
        if self.oracle_text:
            out.append(self.oracle_text)
        if self.flavor_text:
            out.append(italic(self.flavor_text, self.isatty))
        if self.power and self.toughness:
            out.append(self.power + "/" + self.toughness)

        return "\n".join(out)


def bold(s, isatty):
    if isatty:
        return "\x1B[1m" + s + "\x1B[0m"
    return s


def italic(s, isatty):
    if isatty:
        return "\x1B[3m" + s + "\x1B[0m"
    return s
