import datetime

from . import parser, storage

aliases = {
    'config': ('config', ),
    'login': ('login', 'in', 'i'),
    'logout': ('logout', 'out', 'o'),
    'inout': ('inout', 'io'),
    'description': ('description', 'd'),
    'build': ('build', ),
    'help': ('help', 'h'),
}


def config(uuid, argv):
    cmdarg = parser.CommandArguments()
    cmdarg.define('key')
    cmdarg.define('value')
    args = cmdarg.parse(argv)

    user = storage.User(uuid)
    user.config(args.key, args.value)

    return {'key': args.key, 'value': args.value}


def login(uuid, argv, timestamp):
    cmdarg = parser.CommandArguments()
    cmdarg.define('time', optional=True, type=datetime.datetime)
    args = cmdarg.parse(argv)

    dt = args.time or datetime.datetime.fromtimestamp(timestamp)

    user = storage.User(uuid)
    user.login(dt)

    return {'time': str(dt)}


def logout(uuid, argv, timestamp):
    cmdarg = parser.CommandArguments()
    cmdarg.define('time', optional=True, type=datetime.datetime)
    args = cmdarg.parse(argv)

    dt = args.time or datetime.datetime.fromtimestamp(timestamp)

    user = storage.User(uuid)
    user.logout(dt)

    return {'time': str(dt)}


def inout(uuid, argv):
    cmdarg = parser.CommandArguments()
    cmdarg.define('date')
    cmdarg.define('time_from')
    cmdarg.define('time_to')
    args = cmdarg.parse(argv)


def description(uuid, argv):
    cmdarg = parser.CommandArguments()
    cmdarg.define('message')
    cmdarg.define('date', optional=True, type=datetime.date)
    args = cmdarg.parse(argv)

    date = args.date or datetime.date.today()

    user = storage.User(uuid)
    user.description(args.message, date)

    return {'message': args.message, 'date': date}


def build(uuid, argv):
    cmdarg = parser.CommandArguments()
    cmdarg.define('month', optional=True)
    args = cmdarg.parse(argv)


def help(argv):
    cmdarg = parser.CommandArguments()
    args = cmdarg.parse(argv)
