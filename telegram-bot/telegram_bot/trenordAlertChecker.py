"""
A module to interact and check the status of train lines
"""
import MySQLdb
import time
from datetime import datetime
import datetime as dt

# import telepot
from emoji import emojize
from .buttons import *
import urllib.request, urllib.parse, urllib.error
from .bot_utility import create_bot
from .bot_utility import connect_db

# import loginInfo


def updateAlertsDatabase():
    """
    Check if there are updates on the train lines
    """
    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE TRENOBOT;")

    now = dt.datetime.now()
    nowDB = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM directress_alerts")
    dbLines = cursor.fetchall()

    for row in dbLines:
        print("Controllo %s" % row["name"])
        now = dt.datetime.now()
        page = urllib.request.urlopen(row["trenord_link"]).read().decode("utf-8")

        if now.hour < 10:
            hour = "0%s" % (now.hour)
        else:
            hour = now.hour

        if now.month < 10:
            month = "0%s" % (now.month)
        else:
            month = now.month

        dateString = "%s/%s/%s %s" % (now.day, month, now.year, hour)

        lastAlert = ""

        if dateString in page:
            page = page[page.index(dateString) :]
            lastAlert = page[page.index("<p> <p>") + 7 : page.index("</p></p>")]

        if "emergenza sanitaria" not in lastAlert.lower():
            if (
                "avverse" in lastAlert.lower()
                or "retifica" in lastAlert.lower()
                or "disagi" in lastAlert.lower()
                or "<strong>" in lastAlert.lower()
                or "cancellato" in lastAlert.lower()
                or "non sar" in lastAlert.lower()
                or "non partir" in lastAlert.lower()
                or "sospesa" in lastAlert.lower()
                or "termina" in lastAlert.lower()
            ):
                lastAlert = lastAlert.replace("<p>", "")
                lastAlert = lastAlert.replace("<strong>", "")
                lastAlert = lastAlert.replace("</strong>", "")
                lastAlert = lastAlert.replace("'", " ")
                lastAlert = lastAlert.replace("</p>", "")
                lastAlert = lastAlert.replace("<br/>", "")
                lastAlert = lastAlert.replace("&nbsp", "")
            else:
                lastAlert = None
        else:
            lastAlert = None

        if lastAlert is not None:
            print(lastAlert)
            print("\n")
            try:
                cursor.execute(
                    'UPDATE directress_alerts SET last_alert_text="%s", last_update_datetime="%s" WHERE id="%s"'
                    % (lastAlert, nowDB, row["id"])
                )  # Use REPLACE instead of INSERT for update old records if exists
                database.commit()
            except Exception as e:
                pass
            else:
                print("       Nessun alert su questa direttrice")

    database.close()


def sendMessageKeyboard(chatId, msg, keyboard):
    """
    Send updates to a certain chat
    """
    bot = create_bot()
    bot.sendMessage(
        chatId,
        emojize(msg, use_aliases=True),
        parse_mode="html",
        disable_web_page_preview=None,
        disable_notification=None,
        reply_markup=keyboard,
    )


def main():
    """
    Run the checks for the train lines
    """
    updateAlertsDatabase()

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE TRENOBOT;")

    nowDB = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    nowDB = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT * FROM user_directress_alert")
    dbLinesUsers = cursor.fetchall()

    mess = ""
    for row in dbLinesUsers:
        cursor.execute(
            "SELECT * FROM directress_alerts WHERE id=%s" % (row["directress_id"])
        )
        dbLinesDirectress = cursor.fetchone()

        if (
            dbLinesDirectress["last_alert_text"] is not None
            and dbLinesDirectress["last_alert_text"] is not ""
        ):
            if row["last_alert_text"] != dbLinesDirectress["last_alert_text"]:
                print(dbLinesDirectress["last_alert_text"])
                mess += ":warning: Direttrice <b>%s</b>\n\n%s" % (
                    dbLinesDirectress["name"],
                    dbLinesDirectress["last_alert_text"],
                )
                sendMessageKeyboard(row["user_id"], mess, trenordAlertButtons())
                cursor.execute(
                    "UPDATE user_directress_alert SET last_alert_text='%s', last_alert_datetime='%s' WHERE user_id='%s' AND directress_id=%s"
                    % (
                        dbLinesDirectress["last_alert_text"],
                        nowDB,
                        row["user_id"],
                        row["directress_id"],
                    )
                )
                database.commit()
    database.close()


if __name__ == "__main__":
    main()
