import os
import sys

from . import storage
from .slackbot import SlackBot


def eprint(*args, exit=False, **kargs):
    print(*args, file=sys.stderr, **kargs)
    if exit:
        sys.exit(1)


def main():
    token = os.environ.get('ACTREP_SLACKBOT_TOKEN')
    interval = os.environ.get('ACTREP_SLACKBOT_INTERVAL')
    home_dir = os.environ.get('ACTREP_ROOT') or os.path.expanduser('~/.actrep')

    if token is None:
        eprint(
            'Error: please set the ACTREP_SLACKBOT_TOKEN environment variable.', exit=True)

    storage.init_db('{}/.sqlite'.format(home_dir))
    slackbot = SlackBot(token)

    if interval:
        slackbot.run(float(interval))
    else:
        slackbot.run()


if __name__ == '__main__':
    main()
