import time

from slackclient import SlackClient

from . import command
from .command import NotEnoughArgumentError


class ConnectionFailedError(Exception):
    pass


class SlackBot(object):

    def __init__(self, token):
        self.client = SlackClient(token)
        self.token = token

    def run(self, interval=1):
        if self.client.rtm_connect():
            while True:
                data = self.client.rtm_read()
                if len(data) > 0:
                    self._parse_response(data)
                time.sleep(interval)
        else:
            raise ConnectionFailedError()

    def _parse_response(self, data):
        for item in data:
            if ('type' in item) and (item['type'] == 'message') and ('subtype' not in item):
                cmd, argv = self._parse_message(item['text'])
                timestamp = float(item['ts'])

                try:
                    if cmd in command.aliases['config']:
                        command.config(argv)

                    elif cmd in command.aliases['login']:
                        command.login(argv, timestamp)

                    elif cmd in command.aliases['logout']:
                        command.logout(argv, timestamp)

                    elif cmd in command.aliases['inout']:
                        command.inout(argv)

                    elif cmd in command.aliases['description']:
                        command.description(argv)

                    elif cmd in command.aliases['build']:
                        command.build(argv)

                    elif cmd in command.aliases['help']:
                        command.help(argv)

                except NotEnoughArgumentError as e:
                    self.reply(item['channel'], item['user'], e)

    def _parse_message(self, message):
        args = message.strip().split()
        return args[0].lower(), args[1:]

    def reply(self, channel, user, text):
        message = '<@{}>: {}'.format(user, text)
        self.client.rtm_send_message(channel, message)
