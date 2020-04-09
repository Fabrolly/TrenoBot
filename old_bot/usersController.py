import MySQLdb
import time
from bot_utility import connect_db

# import loginInfo


def addUserIfNotExist(msg):

    # Connecting to database
    database = connect_db()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    now = time.strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("USE TRENOBOT;")
        cursor.execute(
            "INSERT IGNORE INTO users (id, name, registration_date) VALUES (%s, '%s', '%s');"
            % (msg["chat"]["id"], msg["chat"]["first_name"], now)
        )  # Use REPLACE instead of INSERT for update old records if exists, TODO: remove warning from terminal
        database.commit()
    except MySQLdb.Error as e:
        database.rollback()
        return "Got Error {!r}, errno is {}".format(e, e.args[0])

    database.close()
    return "added"
