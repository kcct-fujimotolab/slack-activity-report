import datetime
import tempfile

import dateutil.parser

from . import convert, formatter, parser, storage

aliases = {
    'config': ('config', ),
    'login': ('login', 'in', 'i'),
    'logout': ('logout', 'out', 'o'),
    'inout': ('inout', 'io'),
    'description': ('description', 'd'),
    'build': ('build', ),
    'list': ('list', 'ls', 'l'),
}


class Command(object):

    def __init__(self, uuid):
        self.uuid = uuid
        self.user = storage.User(uuid)

    def execute(self, args):
        if isinstance(args, str):
            args = parser.parse_str(args)

        if not isinstance(args, list):
            raise TypeError('args should be list or str')

        cmd = args[0].lower()
        argv = args[1:]

        if cmd in aliases['config']:
            key, value = self.config(*argv)
            return 'Saved as `{}` = `{}`'.format(key, value), 'text'

        elif cmd in aliases['login']:
            dt = self.login(*argv)
            return 'Logged-in at {}'.format(dt), 'text'

        elif cmd in aliases['logout']:
            dt = self.logout(*argv)
            return 'Logged-out at {}'.format(dt), 'text'

        elif cmd in aliases['description']:
            message, date = self.description(*argv)
            return 'Update description: {} ({})'.format(message, date), 'text'

        elif cmd in aliases['build']:
            filepath = self.build(*argv)
            return filepath, 'filepath'

        elif cmd in aliases['list']:
            text = self.list(*argv)
            return text, 'text'

    def config(self, key, value):
        self.user.config(key, value)
        return key, value

    def login(self, dt=datetime.datetime.now()):
        if isinstance(dt, str):
            dt = dateutil.parser.parse(dt)
        self.user.login(dt)
        return dt

    def logout(self, dt=datetime.datetime.now()):
        if isinstance(dt, str):
            dt = dateutil.parser.parse(dt)
        self.user.logout(dt)
        return dt

    def description(self, message, date=datetime.date.today()):
        if isinstance(date, str):
            dt = dateutil.parser.parse(dt).date()
        self.user.description(message, date)
        return message, date

    def build(self, month=datetime.date.today().month):
        activities = self._activities(month)
        activities = [a for a in activities
                      if a[0].date() == a[1].date()]
        days = [a[0].day for a in activities]
        activities = [activities[days.index(i)]
                      if i in days else (None, None, '')
                      for i in range(1, 32)]
        print(activities)

        converter = convert.Converter()
        converter.to_png(self.user.name or '',
                         [a[0] for a in activities],
                         [a[1] for a in activities],
                         [a[2] for a in activities])
        _, filepath = tempfile.mkstemp(suffix='.png')
        converter.save(filepath)
        return filepath

    def list(self, month=None):
        activities = self._activities(month)
        return ('```'
                '{}'
                '```'
                .format(formatter.to_gfm_table(activities)))

    def _activities(self, month=None):
        if month is None:
            since = until = None
        else:
            since, until = self._datetime_range(int(month))
        activities = self.user.activities(since, until)
        activities = [(a['start_time'], a['end_time'], a['content'] or '')
                      for a in activities
                      if a['start_time'] is not None and a['end_time'] is not None]
        return activities

    def _datetime_range(self, month=datetime.date.today().month):
        today = datetime.date.today()
        # 4 <= today.month <= 12
        if today.month in range(4, 12 + 1):
            # 4 <= month <= 12
            if month in range(4, 12 + 1):
                year = today.year
            # 1 <= month <= 3
            else:
                year = today.year + 1
        # 1 <= today.month <= 3
        else:
            # 4 <= month <= 12
            if month in range(4, 12 + 1):
                year = today.year - 1
            # 1 <= month <= 3
            else:
                year = today.year

        since = datetime.datetime.min.replace(year=year, month=month)
        until = datetime.datetime.max.replace(year=year, month=month)
        return since, until
