import webbrowser
import argparse
import time
import sys
import os

SORT_OPTS = [
    "name",
    "set",
    "tix",
    "usd",
    "eur",
    "cmc",
    "pow",
    "tou",
    "rarity",
    "color",
    "edhrec"
]

CATALOG_OPTS = [
    "card-names",
    "word-bank",
    "creature-types",
    "planeswalker-types",
    "land-types",
    "spell-types",
    "artifact-types",
    "powers",
    "toughnesses",
    "loyalties"
]

def autocomplete(shell, args):
    cmd = args[0].strip()
    cur = args[1].strip()
    prev = args[2].strip()

    if prev in ("-s", "--sort"):
        opts = SORT_OPTS
    elif prev == cmd:
        opts = ["search", "named", "random", "catalog", "--tty", "--no-tty", "--urls"]
    elif prev == "search":
        opts = ["--sort"]
    elif prev in ("named", "--exact", "--open"):
        opts = ["--exact", "--open"]
    elif prev == "catalog":
        opts = CATALOG_OPTS
    else:
        opts = []

    opts = filter(lambda s: s.startswith(cur), opts)
    print(*opts, sep="\n")


def do_complete(shell):
    if shell == "bash":
        print("complete -o nosort -C '_SCRYCLI_COMPLETE=source-bash scrycli' scrycli")
    return 0


def main():
    scrycli_complete = os.environ.get("_SCRYCLI_COMPLETE", "")
    if scrycli_complete.startswith("source-"):
        shell = scrycli_complete[len("source-"):]
        if len(sys.argv) > 1:
            return autocomplete(shell, sys.argv[1:])
        return do_complete(shell)

    from .scryfall import Scryfall
    parser = argparse.ArgumentParser("scrycli")

    tty = parser.add_mutually_exclusive_group()
    tty.add_argument(
        "--tty",
        action="store_true",
        default=None,
        dest="tty",
        help="force tty printing on (italics etc.)"
    )
    tty.add_argument(
        "--no-tty",
        action="store_false",
        default=None,
        dest="tty",
        help="force tty printing off"
    )

    parser.add_argument(
        "--urls", "-u",
        action="store_true",
        help="show urls to cards"
    )

    # TODO
    # card_info = parser.add_mutually_exclusive_group()
    # card_info.add_argument(
    #     "--all", "-a",
    #     const="all",
    #     action="store_const",
    #     dest="format",
    #     help="show all information about cards"
    # )
    # card_info.add_argument(
    #     "--full", "-f",
    #     const="full",
    #     action="store_const",
    #     dest="format",
    #     help="show information that the card faces have"
    # )
    # card_info.add_argument(
    #     "--small", "-s",
    #     const="all",
    #     action="store_const",
    #     dest="format",
    #     help="show name, mana cost and type line"
    # )
    # card_info.add_argument(
    #     "--tiny", "-t",
    #     const="tiny",
    #     action="store_const",
    #     dest="format",
    #     default=True,
    #     help="show name and mana cost (default)"
    # )
    # card_info.add_argument(
    #     "--name", "-n",
    #     const="name",
    #     action="store_const",
    #     dest="format",
    #     help="only show the name of the card"
    # )
    # card_info.add_argument(
    #     "--json", "-j",
    #     const="json",
    #     action="store_const",
    #     dest="format",
    #     help="output all information about the card as json"
    # )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command"
    )

    search = subparsers.add_parser("search")
    search.add_argument(
        "--sort", "-s",
        choices=SORT_OPTS,
        default="name",
        help="order in which to sort the results"
    )
    search.add_argument(
        "query",
        nargs=argparse.REMAINDER,
        help="query arguments, for help see https://scryfall.com/docs/reference"
    )

    named = subparsers.add_parser("named")
    named.add_argument(
        "--exact", "-e",
        action="store_true",
        help="no fuzzy matching"
    )
    named.add_argument(
        "--open", "-o",
        action="store_true",
        help="open the card in browser"
    )
    named.add_argument(
        "query",
        nargs=argparse.REMAINDER
    )

    random = subparsers.add_parser("random")
    random.add_argument(
        "count",
        nargs="?",
        type=int,
        default=1,
        help="amount of random cards to get"
    )

    catalog = subparsers.add_parser("catalog")
    catalog.add_argument("catalog", choices=CATALOG_OPTS)

    args = parser.parse_args()

    isatty = sys.stdout.isatty()
    if args.tty is not None:
        isatty = args.tty

    api = Scryfall(isatty, args.urls)

    try:
        if args.command == "search":
            for i in api.search(" ".join(args.query), args.sort):
                print("---")
                print(i)
        elif args.command == "named":
            card = api.named(" ".join(args.query), args.exact)
            print(card)
            if args.open:
                webbrowser.open(card.url)
        elif args.command == "random":
            for i in api.random(args.count):
                print("---")
                print(i)
        elif args.command == "catalog":
            for i in api.catalog(args.catalog):
                print(i)
        else:
            parser.print_help()
            return 1
    except api.APIError:
        return 2
    except api.TooManyRequests:
        print("too many requests\nif you're running scrycli parallelized, don't", file=sys.stderr)
        time.sleep(1)
        return 3


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)
