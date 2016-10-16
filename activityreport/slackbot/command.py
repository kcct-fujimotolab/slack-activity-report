import datetime

from .. import storage


class NotEnoughArgumentError(Exception):
    pass


class CommandArguments(object):

    def __init__(self):
        self._defined_args = []

    def define(self, name, optional=False):
        self._defined_args.append({'name': name, 'optional': optional})

    def parse(self, argv):
        args = _ArgumentsDictionary()
        n_args = len(argv)

        for i, defined_arg in enumerate(self._defined_args):
            # when get the argument
            if n_args > i:
                args[defined_arg['name']] = argv[i]

            # when cannot get the optional argument
            elif defined_arg['optional']:
                args[defined_arg['name']] = None

            # when cannot get the required argument
            else:
                raise NotEnoughArgumentError(
                    'require the <{}> argument'.format(defined_arg['name']))

        return args


class _ArgumentsDictionary(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delattr__


aliases = {
    'config': ('config'),
    'login': ('login', 'in', 'i'),
    'logout': ('logout', 'out', 'o'),
    'inout': ('inout', 'io'),
    'description': ('description', 'd'),
    'build': ('build'),
    'help': ('help', 'h'),
}


def config(uuid, argv):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('key')
        cmdarg.define('value')
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise

    user = storage.User(uuid)
    user.config(args.key, args.value)


def login(uuid, argv, timestamp):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('time', optional=True)
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise

    user = storage.User(uuid)
    user.login(datetime.datetime.fromtimestamp(timestamp))


def logout(uuid, argv, timestamp):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('time', optional=True)
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise

    user = storage.User(uuid)
    user.logout(datetime.datetime.fromtimestamp(timestamp))


def inout(uuid, argv):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('date')
        cmdarg.define('time_from')
        cmdarg.define('time_to')
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise


def description(uuid, argv):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('message')
        cmdarg.define('date', optional=True)
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise

    user = storage.User(uuid)
    user.description(args.message, date=args.date)


def build(uuid, argv):
    try:
        cmdarg = CommandArguments()
        cmdarg.define('month', optional=True)
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise


def help(argv):
    try:
        cmdarg = CommandArguments()
        args = cmdarg.parse(argv)

    except NotEnoughArgumentError:
        raise
