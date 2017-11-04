def bold(s, isatty):
    if isatty:
        return "\x1B[1m" + s + "\x1B[0m"
    return s


def italic(s, isatty):
    if isatty:
        return "\x1B[3m" + s + "\x1B[0m"
    return s
