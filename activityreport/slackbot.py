import time

from slackclient import SlackClient
from websocket._exceptions import WebSocketConnectionClosedException

from slacker import Slacker

from . import command


class ConnectionFailedError(Exception):
    pass


class SlackBot(object):

    def __init__(self, token):
        self.client = SlackClient(token)
        self.slack = Slacker(token)
        self.token = token
        self.all_members = self.slack.users.list().body['members']
        self.members = [m for m in self.all_members if not m.get('is_bot')]
        self.bots = [m for m in self.all_members if m.get('is_bot')]

    def run(self, interval=1, max_retry_count=5):
        self._connect()
        retry_count = 0

        while True:
            try:
                data = self.client.rtm_read()
                if len(data) > 0:
                    self._parse_response(data)
                retry_count = 0
                time.sleep(interval)
            except WebSocketConnectionClosedException:
                if retry_count < max_retry_count:
                    self._connect()
                    sleep(1)
                    retry_count += 1
                else:
                    raise ConnectionFailedError()

    def _connect(self):
        result = self.client.rtm_connect()

        if not result:
            raise ConnectionFailedError()

    def _parse_response(self, data):
        member_ids = [m['id'] for m in self.members]
        for item in data:
            if item.get('type') == 'message' and item.get('user') in member_ids:
                cmd = command.Command(item['user'])
                try:
                    response, content_type = cmd.execute(item['text'])
                except Exception as e:
                    self.reply(item['channel'], item['user'], e)
                else:
                    if response is not None:
                        if content_type == 'text':
                            self.reply(item['channel'], item['user'], response)
                        elif content_type == 'filepath':
                            self.upload_file(item['channel'], response)

    def reply(self, channel, user, text):
        message = '<@{}>: {}'.format(user, text)
        self.client.rtm_send_message(channel, message)

    def upload_file(self, channel, filepath):
        self.slack.files.upload(filepath, channels=channel)
