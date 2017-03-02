import shlex


def parse_str(string):
    args = shlex.split(string)
    return args
