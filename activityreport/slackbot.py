import time

from slackclient import SlackClient
from websocket._exceptions import WebSocketConnectionClosedException

from . import command, parser


class ConnectionFailedError(Exception):
    pass


class SlackBot(object):

    def __init__(self, token):
        self.client = SlackClient(token)
        self.token = token

    def run(self, interval=1, max_retrieval=5):
        self._connect()
        retrieval_count = 0

        while True:
            try:
                data = self.client.rtm_read()
                if len(data) > 0:
                    self._parse_response(data)
                retrieval_count = 0
                time.sleep(interval)
            except WebSocketConnectionClosedException:
                if retrieval_count < max_retrieval:
                    self._connect()
                    sleep(1)
                    retrieval_count += 1
                else:
                    raise ConnectionFailedError()

    def _connect(self):
        result = self.client.rtm_connect()

        if not result:
            raise ConnectionFailedError()

    def _parse_response(self, data):
        for item in data:
            if ('type' in item) and (item['type'] == 'message') and ('subtype' not in item):
                cmd, argv = parser.parse_str(item['text'])
                timestamp = int(float(item['ts']))
                uuid = item['user']

                try:
                    if cmd in command.aliases['config']:
                        res = command.config(uuid, argv)
                        self.reply(item['channel'], uuid, 'ok'.format(**res))

                    elif cmd in command.aliases['login']:
                        res = command.login(uuid, argv, timestamp)
                        self.reply(item['channel'], uuid,
                                   'logged-in at {time}'.format(**res))

                    elif cmd in command.aliases['logout']:
                        res = command.logout(uuid, argv, timestamp)
                        self.reply(item['channel'], uuid,
                                   'logged-out at {time}'.format(**res))

                    elif cmd in command.aliases['inout']:
                        command.inout(uuid, argv)

                    elif cmd in command.aliases['description']:
                        res = command.description(uuid, argv)
                        self.reply(
                            item['channel'], uuid, 'Update description at {date}: {message}'.format(**res))

                    elif cmd in command.aliases['build']:
                        command.build(uuid, argv)

                    elif cmd in command.aliases['help']:
                        command.help(argv)

                except Exception as e:
                    self.reply(item['channel'], uuid, e)

    def reply(self, channel, user, text):
        message = '<@{}>: {}'.format(user, text)
        self.client.rtm_send_message(channel, message)
