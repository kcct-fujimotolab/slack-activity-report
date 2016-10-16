import datetime
import os
import sqlite3

import dateutil.parser

connection = None


def init_db(db_file):
    global connection
    if connection is None:
        try:
            os.makedirs(os.path.dirname(db_file))
        except:
            pass

        connection = sqlite3.connect(db_file, detect_types=(
            sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES), isolation_level=None)
        sqlite3.dbapi2.converters[
            'DATETIME'] = sqlite3.dbapi2.converters['TIMESTAMP']

        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS activities(
                          id INTEGER PRIMARY KEY,
                          user_id INTERGER NOT NULL,
                          start_time DATETIME,
                          end_time DATETIME,
                          content TEXT
                       )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS users(
                          id INTEGER PRIMARY KEY,
                          slack_uuid TEXT UNIQUE,
                          name TEXT
                       )''')
        cursor.close()


class User(object):

    def __init__(self, slack_uuid):
        self.slack_uuid = slack_uuid

        cursor = connection.cursor()
        cursor.execute('''INSERT INTO users(slack_uuid)
                       SELECT :uuid WHERE NOT EXISTS (
                       SELECT 1 FROM users WHERE slack_uuid = :uuid)''', {'uuid': self.slack_uuid})
        cursor.execute(
            '''SELECT * FROM users WHERE slack_uuid = ?''', (self.slack_uuid, ))
        self.id, _, self.name = cursor.fetchone()
        cursor.close()

    def login(self, time):
        cursor = connection.cursor()

        cursor.execute('''SELECT id FROM activities
                       WHERE
                         user_id = :user_id AND (DATE(start_time) = DATE(:time) OR DATE(end_time) = DATE(:time))
                       ''', {'user_id': self.id, 'time': time})
        activity_ids = cursor.fetchall()

        if len(activity_ids) == 0:
            cursor.execute('''INSERT INTO activities(user_id, start_time)
                           SELECT users.id, :time
                           FROM users
                           WHERE users.slack_uuid = :uuid''', {'time': time, 'uuid': self.slack_uuid})
        else:
            cursor.execute('''UPDATE activities
                           SET start_time = ?
                           WHERE id = ?''', (time, activity_ids[0][0]))

        cursor.close()

    def logout(self, time):
        cursor = connection.cursor()

        cursor.execute('''SELECT id FROM activities
                       WHERE
                         user_id = :user_id AND (DATE(start_time) = DATE(:time) OR DATE(end_time) = DATE(:time))
                       ''', {'user_id': self.id, 'time': time})
        activity_ids = cursor.fetchall()

        if len(activity_ids) == 0:
            cursor.execute('''INSERT INTO activities(user_id, end_time)
                           SELECT users.id, :time
                           FROM users
                           WHERE users.slack_uuid = :uuid''', {'time': time, 'uuid': self.slack_uuid})
        else:
            cursor.execute('''UPDATE activities
                           SET end_time = ?
                           WHERE id = ?''', (time, activity_ids[0][0]))

        cursor.close()

    def description(self, content, date=None):
        dt = date or datetime.datetime.now()
        cursor = connection.cursor()
        cursor.execute('''UPDATE activities
                       SET content = :content
                       WHERE DATE(start_time) = DATE(:time) OR DATE(end_time) = DATE(:time)''', {'content': content, 'time': dt})

        cursor.close()

    def config(self, key, value):
        if key == 'name':
            cursor = connection.cursor()
            cursor.execute(
                'UPDATE users SET name = ? WHERE id = ?', (value, self.id))
            cursor.close()
            self.name = value
