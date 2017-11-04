class ScryfallSet:
    def __init__(self, data):
        self.name = data["name"]
        self.code = data["code"]
        self.released_at = data.get("released_at", None)
        self.block = data.get("block", None)
        self.block_code = data.get("block_code", None)
        self.parent_set_code = data.get("parent_set_code", None)

    def __str__(self):
        out = []
        out.append("{} ({})".format(self.name, self.code))
        if self.released_at:
            out.append("Released: {}".format(self.released_at))
        if self.block and self.block_code:
            out.append("Block: {} ({})".format(self.block, self.block_code))
        if self.parent_set_code:
            out.append("Parent Set: {}".format(self.parent_set_code))  # TODO: add parent set name

        return "\n".join(out)