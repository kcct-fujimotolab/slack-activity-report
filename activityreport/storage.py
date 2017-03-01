import os
import sqlite3

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
                       SELECT id FROM users WHERE slack_uuid = :uuid)''', {'uuid': self.slack_uuid})
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

    def description(self, content, date):
        cursor = connection.cursor()
        cursor.execute('''UPDATE activities
                       SET content = :content
                       WHERE user_id = :id AND (DATE(start_time) = DATE(:time) OR DATE(end_time) = DATE(:time))''', {'content': content, 'time': date, 'id': self.id})

        cursor.close()

    def config(self, key, value):
        if key == 'name':
            cursor = connection.cursor()
            cursor.execute(
                'UPDATE users SET name = ? WHERE id = ?', (value, self.id))
            cursor.close()
            self.name = value

    def activities(self, since=None, until=None):
        cursor = connection.cursor()
        if since is None and until is None:
            cursor.execute('''SELECT * FROM activities
                           WHERE
                           user_id = :user_id
                           ''', {'user_id': self.id})
        else:
            cursor.execute('''SELECT * FROM activities
                           WHERE
                           user_id = :user_id AND (DATE(:since) <= DATE(start_time) AND DATE(end_time) <= DATE(:until))
                           ''', {'user_id': self.id, 'since': since, 'until': until})
        acts = cursor.fetchall()
        cursor.close()

        acts = [{
            'activity_id': a[0],
            'user_id': a[1],
            'start_time': a[2],
            'end_time': a[3],
            'content': a[4],
        } for a in acts]

        return acts
