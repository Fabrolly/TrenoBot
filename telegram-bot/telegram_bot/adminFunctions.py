"""
A module that exposes various functions that can only be accessed by admins.
"""
import MySQLdb
from emoji import emojize
from .bot_utility import create_bot
from .bot_utility import connect_db


def systemStats():
    """
    Gather stats from the database
    """
    msg = "<b>Statistiche</b>\n\n"
    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("USE TRENOBOT;")
        usersNumber = cursor.execute(
            "SELECT * from users;"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "Utenti registrati: <b>%s</b>" % (usersNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    try:
        trainsNumber = cursor.execute(
            "SELECT * from trains;"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "\n\nTreni in locale: <b>%s</b>" % (trainsNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    try:
        updatedTrainsNumber = cursor.execute(
            "SELECT * from trains WHERE last_update >= CURDATE();"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "\nDi cui aggiornati oggi: <b>%s</b>" % (updatedTrainsNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    try:
        prgNumber = cursor.execute(
            "SELECT * from user_train;"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "\n\nTreni Monitorati: <b>%s</b>" % (prgNumber)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    try:
        fini = cursor.execute(
            "SELECT * from user_train WHERE arrival_datetime >= CURDATE();"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "\nDi cui gia' a destinazione: <b>%s</b>" % (fini)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    try:
        direcNumbers = cursor.execute(
            "SELECT * from user_directress_alert;"
        )  # Use REPLACE instead of INSERT for update old records if exists
        msg += "\n\nDirettrici monitorate da utenti: <b>%s</b>" % (direcNumbers)
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        msg += error

    database.close()
    return (msg, "")


def broadcast(msg):
    """
    Send a broadcast message to all the users

    Params:
        msg: the message to send
    """
    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    msgAdmin = "<b>Messaggio mandato a:</b>\n\n"
    try:
        cursor.execute("USE TRENOBOT;")
        usersNumber = cursor.execute(
            "SELECT id from users;"
        )  # Use REPLACE instead of INSERT for update old records if exists
        dbLines = cursor.fetchall()
    except MySQLdb.Error as e:
        database.rollback()
        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
        return (error, "")

    bot = create_bot()

    for row in dbLines:
        bot.sendMessage(
            row["id"],
            emojize(msg, use_aliases=True),
            parse_mode="html",
            disable_web_page_preview=None,
            disable_notification=None,
        )
        msgAdmin += "Mandato a %s\n" % (row["id"])

    return (msgAdmin, "")
