import os
import sys

import click

from . import slackbot, storage

home_dir = os.environ.get('ACTREP_ROOT') or os.path.expanduser('~/.actrep')


def eprint(*args, exit=False, **kargs):
    print(*args, file=sys.stderr, **kargs)
    if exit:
        sys.exit(1)


@click.group()
def main():
    pass


@main.command()
@click.option('--token', '-t', envvar='ACTREP_SLACKBOT_TOKEN',
              help='The slackbot\'s token. Defaults to ACTREP_SLACKBOT_TOKEN environment variable.')
@click.option('--interval', '-i', envvar='ACTREP_SLACKBOT_INTERVAL', default=1.0, type=float,
              help='The interval of the bot confirms input from users. Defaults to ACTREP_SLACKBOT_INTERVAL environment variable or 1.0.')
@click.option('--retry-count', '-r', default=5, type=int,
              help='The number of maximum retry count. Default to 5.')
def start(token, interval, retry_count):
    if token is None:
        eprint(
            'Error: please set the ACTREP_SLACKBOT_TOKEN environment variable or --token option.', exit=True)

    storage.init_db(os.path.join(home_dir, '.sqlite'))
    bot = slackbot.SlackBot(token)

    bot.run(interval, retry_count)


if __name__ == '__main__':
    main()
