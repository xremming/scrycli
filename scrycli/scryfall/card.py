from ..utils import italic, bold


class ScryfallCard:

    LONGEST_MANA_COST = len("{W}{W}{U}{U}{B}{B}{R}{R}{G}{G}")
    LONGEST_NAME = len("Our Market Research Shows That Players Like Really Long Card Names So We Made this Card to Have the Absolute Longest Card Name Ever Elemental")
    LONGEST_TYPE_LINE = len("Legendary Enchantment Creature — God")

    class CardFace:

        def __init__(self, data, isatty=False, urls=False):
            self.isatty = isatty
            self.urls = urls

            self.name = data["name"]
            self.mana_cost = data.get("mana_cost", None)
            self.type_line = data["type_line"]
            self.oracle_text = data.get("oracle_text", None)
            self.power = data.get("power", None)
            self.toughness = data.get("toughness", None)
            self.loyalty = data.get("loyalty", None)

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
            if self.loyalty:
                out.append(self.loyalty)
            if self.urls:
                out.append(self.url)

            return "\n".join(out)

    def __init__(self, data, isatty=False, urls=False):
        self.isatty = isatty
        self.urls = urls

        self._data = data
        self.name = data["name"]
        self.mana_cost = data.get("mana_cost", None)
        self.type_line = data.get("type_line", None)
        self.oracle_text = data.get("oracle_text", None)
        self.flavor_text = data.get("flavor_text", None)
        self.power = data.get("power", None)
        self.toughness = data.get("toughness", None)
        self.loyalty = data.get("loyalty", None)

        self.url = data.get("scryfall_uri", None)

        self.card_faces = []
        for face in data.get("card_faces", []):
            self.card_faces.append(self.CardFace(face, isatty, urls))

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
        if self.loyalty:
            out.append(self.loyalty)
        if self.urls:
            out.append(self.url)

        return "\n".join(out)
