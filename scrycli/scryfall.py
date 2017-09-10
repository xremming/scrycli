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
        f"scrycli/{__version__} (github.com/polarpayne/scrycli) "
        f"requests/{requests.__version__} "
        f"python/{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    SLEEP = 0.1

    def __init__(self):
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
            raise self.APIError(f"API returned status code {response.status_code}.")

    def _get_url(self, url):
        return self._check(
            self._r.get(url)
        )

    def _get(self, api, params=None):
        if params is None:
            params = {}

        return self._check(
            self._r.get(f"{self.API_URL}{api}", params=params)
        )

    def search(self, q):
        data = self._get("/cards/search", params={"q": q})

        yield from (ScryfallCard(card) for card in data["data"])

        more = data.get("has_more", False)
        next_page = data.get("next_page", None)
        while more and next_page:
            time.sleep(self.SLEEP)
            data = self._get_url(next_page)
            more = data.get("has_more", False)
            next_page = data.get("next_page", None)
            yield from (ScryfallCard(card) for card in data["data"])

    def random(self, count=1):
        for _ in range(count):
            yield ScryfallCard(self._get("/cards/random"))
            time.sleep(self.SLEEP)


class ScryfallCard:

    LONGEST_MANA_COST = len("{W}{W}{U}{U}{B}{B}{R}{R}{G}{G}")
    LONGEST_NAME = len("Our Market Research Shows That Players Like Really Long Card Names So We Made this Card to Have the Absolute Longest Card Name Ever Elemental")
    LONGEST_TYPE_LINE = len("Legendary Enchantment Creature — God")

    def __init__(self, data, formatting="small"):
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
            self.card_faces.append({
                "name": face["name"],
                "mana_cost": face.get("mana_cost", None),
                "type_line": face["type_line"],
                "oracle_text": face.get("oracle_text", None),
                "power": face.get("power", None),
                "toughness": face.get("toughness", None)
            })

    def __str__(self):
        if len(self.card_faces) > 0:
            return self._multi_face_str()

        out = []
        out.append(self.name + (f" {self.mana_cost}" if self.mana_cost else ""))
        if self.type_line:
            out.append(self.type_line)
        if self.oracle_text:
            out.append(self.oracle_text)
        if self.flavor_text:
            out.append("\x1B[3m" + self.flavor_text + "\x1B[23m")
        if self.power is not None and self.toughness is not None:
            out.append(f"{self.power}/{self.toughness}")

        return "\n".join(out)

    def _multi_face_str(self):
        out = []
        for face in self.card_faces:
            out_face = []
            out_face.append(face["name"] + (f" {face['mana_cost']}" if face["mana_cost"] else ""))
            out_face.append(face["type_line"])
            if face["oracle_text"]:
                out_face.append(face["oracle_text"])
            if face["power"] is not None and face["toughness"] is not None:
                out_face.append(f"{face['power']}/{face['toughness']}")
            out.append("\n".join(out_face))

        return "\n***\n".join(out)
