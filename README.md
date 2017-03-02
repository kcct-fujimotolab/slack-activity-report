# slack-activity-report
slack-activity-report is a Slackbot that interactively records day-to-day activities and build activity reports that conform to the KCCT D5 format.

## Requirements
- Python3

## Installation
You can install and upgrade with pip:
```
pip install -U git+https://github.com/kcct-fujimotolab/slack-activity-report.git
```

### Setting
First, you are going to [create a new slackbot](https://my.slack.com/services/new/bot).

And set some environment variables before running slackbot:
```sh
export ACTREP_SLACKBOT_TOKEN=<token of slackbot>
export ACTREP_ROOT=<directory where settings are saved>
export ACTREP_SLACKBOT_INTERVAL=<interval at which the bot confirms input from the user>
```
`ACTREP_SLACKBOT_TOKEN` must be set to a valid token obtained from Slack.
Other environment variables, if not set, will be `ACTREP_ROOT` is `~/.actrep` and `ACTREP_SLACKBOT_INTERVAL` is `1`.

### Running
You can start slackbot from the command line:
```
slackbot-activity-report start
```

## Usage of Slackbot
You can use the following command with a direct message with slackbot:
- `config`: Configure user data
- `login`, `in`, `i`: Record start time
- `logout`, `out`, `o`: Record end time
- `description`, `d`: Record activities
- `build`: Build and export the monthly activity report (not implemented yet)
- `help`, `h`: Show help message about slackbot commands (not implemented yet)

### Example
```
Me : config user.name 'a KCCT Student'
Bot: @me: ok
```

```
Me : i
Bot: @me: logged-in at 2016-11-16 09:00:00
```

```
Me : i 'nov 15 07:00'
Bot: @me: logged-in at 2016-11-15 07:00:00
```

```
Me : o
Bot: @me: logged-in at 2016-11-16 14:35:00
```

```
Me : o '20161116 1700'
Bot: @me: logged-in at 2016-11-16 17:00:00
```

```
Me : d test
Bot: @me: Update description at 2016-11-16: test
```

```
Me : d 'test 2' 'nov 15'
Bot: @me: Update description at 2016-11-15: test 2
```

### Command

#### config
```
config <key> <value>
```
- `key`: The option's key
- `value`: The option's value corresponds `key`

You can configure following options:
- `user.name` (required): Your full name (use this value when build activity report)

#### login
```
login [<time>]
```
- `time` (optional): Appoint the login time; Default is the time that received the `login` command

#### logout
```
logout [<time>]
```
- `time` (optional): Appoint the logout time; Default is the time that received the `logout` command

#### description
```
description <message> [<date>]
```
- `message`: Use the given `message` as the content of activities
- `date` (optional): Appoint the activity date

#### build
```
build [<month>]
```
- `month`: Build the `month` report
