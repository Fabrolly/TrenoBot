"""
A module for defining the background checks of the train
"""
from .databaseController import *
from .buttons import *
import MySQLdb

# import databaseController
import time
from datetime import datetime
import datetime as dt
import telepot
from emoji import emojize

# import buttons
from .bot_utility import connect_db
from .bot_utility import create_bot

# import loginInfo


def run():
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE TRENOBOT;")

    now = dt.datetime.now()
    # bot = telepot.Bot(loginInfo.telegramKey())
    bot = create_bot()
    cursor.execute("SELECT * FROM user_train")
    dbLines = cursor.fetchall()

    day = "0"
    if now.strftime("%A") == "Monday":
        day = "1"
    if now.strftime("%A") == "Tuesday":
        day = "2"
    if now.strftime("%A") == "Wednesday":
        day = "3"
    if now.strftime("%A") == "Thursday":
        day = "4"
    if now.strftime("%A") == "Friday":
        day = "5"
    if now.strftime("%A") == "Saturday":
        day = "6"
    if now.strftime("%A") == "Sunday":
        day = "7"

    for row in dbLines:
        if day in row["days"]:  # IF IS A TRAIN FOR TODAY
            print("da fare oggi")
            departure_datetime = row["departure_datetime"].replace(
                day=now.day, month=now.month, year=now.year
            )  # In DB I use DATETIME format that contain day and mouth but I must check only the time difference from NOW for the next instruction, then i replace it with current date
            start_time_difference = (
                departure_datetime - now
            ).total_seconds() / 60.0  # difference (in minute) by now

            # -----  preventive check before departure
            if (
                start_time_difference - 15 >= 0 and start_time_difference - 15 <= 2
            ):  # If the train leaves in 15 minutes, check if the train IS REGULAR OR NOT
                requestedTrain = createTrain(
                    row["train_number"]
                )  # create the object Train by the number in DB
                if row["last_alert"] != (
                    requestedTrain.state.lower() + requestedTrain.alert.lower()
                ):  # IF THE TRAIN IS NOT REGULAR I ALERT THE USER THAT THE STATE IS CHANGED
                    keyboard = alertMenuButtons(requestedTrain.number)
                    bot.sendMessage(
                        row["user_id"],
                        emojize(
                            ":warning:<b>ATTENZIONE</b>:warning:\nil Treno %s delle: %s:%s\n<b>Direzione:</b> %s\n\n<i>Risulta</i> <b>%s</b>\n\n<b>Ritardo:</b> %s\n\n%s"
                            % (
                                requestedTrain.number,
                                requestedTrain.departure_datetime.hour,
                                requestedTrain.departure_datetime.minute,
                                requestedTrain.destination,
                                requestedTrain.state,
                                requestedTrain.delay,
                                requestedTrain.alert,
                            ),
                            use_aliases=True,
                        ),
                        parse_mode="html",
                        disable_web_page_preview=True,
                        disable_notification=None,
                        reply_markup=keyboard,
                    )  # invio il messaggio
                    try:
                        cursor.execute(
                            "UPDATE user_train SET last_alert='%s%s' WHERE user_id='%s' AND train_id='%s';"
                            % (
                                requestedTrain.state.lower(),
                                requestedTrain.alert.lower(),
                                row["user_id"],
                                row["train_id"],
                            )
                        )  # Use REPLACE instead of INSERT for update old records if exists
                        database.commit()
                    except MySQLdb.Error as e:
                        database.rollback()
                        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
                        print(error)

            # ----- pre-departure message
            if (
                start_time_difference - 5 >= 0 and start_time_difference - 5 <= 2
            ):  # If the train leaves in 5 minutes, SEND THE DEPARTINGMSG TO USER
                requestedTrain = createTrain(
                    row["train_number"]
                )  # create the object Train by the number in DB
                try:
                    if "Error" in requestedTrain:
                        msg = requestedTrain
                except:
                    msg = requestedTrain.departingMsg(
                        row["origin"], row["destination"]
                    )  # if its all ok i call the method of the Train object for create the message for departing trains
                try:
                    keyboard = alertMenuButtons(requestedTrain.number)
                    bot.sendMessage(
                        row["user_id"],
                        emojize("%s" % (msg), use_aliases=True),
                        parse_mode="html",
                        disable_web_page_preview=True,
                        disable_notification=None,
                        reply_markup=keyboard,
                    )  # invio il messaggio
                except Exception as e:
                    # TODO: da gestire se son bloccato, anche il telegram.py devo gestire questa cosa, RICORDARSI
                    # if('blocked' in e):
                    pass

            # -----  if is running
            arrival_datetime = row["arrival_datetime"].replace(
                day=now.day, month=now.month, year=now.year
            )  # In DB I use DATETIME format that contain day and mouth but I must check only the time difference from NOW for the next instruction, then i replace it with current date
            if departure_datetime < now < arrival_datetime:  # IF THE TRAIN IS RUNNING
                print("RUNNING")
                requestedTrain = createTrain(
                    row["train_number"]
                )  # create the object Train by the number in DB

                # ----- if while is running is not regular
                if row["last_alert"].lower() != (
                    requestedTrain.state.lower() + requestedTrain.alert.lower()
                ):  # IF THE TRAIN IS NOT REGULAR I ALERT THE USER THAT THE STATE IS CHANGED
                    keyboard = alertMenuButtons(requestedTrain.number)
                    bot.sendMessage(
                        row["user_id"],
                        emojize(
                            ":warning:<b>ATTENZIONE</b>:warning:\nil Treno %s delle: %s:%s\n<b>Direzione:</b> %s\n\n<i>Risulta</i> <b>%s</b>\n\n<b>Ritardo:</b> %s\n\n%s"
                            % (
                                requestedTrain.number,
                                requestedTrain.departure_datetime.hour,
                                requestedTrain.departure_datetime.minute,
                                requestedTrain.destination,
                                requestedTrain.state,
                                requestedTrain.delay,
                                requestedTrain.alert,
                            ),
                            use_aliases=True,
                        ),
                        parse_mode="html",
                        disable_web_page_preview=True,
                        disable_notification=None,
                        reply_markup=keyboard,
                    )  # invio il messaggio
                    try:
                        cursor.execute(
                            "UPDATE user_train SET last_alert='%s%s' WHERE user_id='%s' AND train_id='%s';"
                            % (
                                requestedTrain.state.lower(),
                                requestedTrain.alert.lower(),
                                row["user_id"],
                                row["train_id"],
                            )
                        )  # Use REPLACE instead of INSERT for update old records if exists
                        database.commit()
                    except MySQLdb.Error as e:
                        database.rollback()
                        error = "Got Error {!r}, errno is {}".format(e, e.args[0])
                        print(error)

                # ----- if the train is halfway for the user trip i update the user
                middle_time_difference = departure_datetime + (
                    (arrival_datetime - departure_datetime) / 2
                )  # finding the middle datetime from arrival and departing
                middle_time_difference = (
                    middle_time_difference - now
                ).total_seconds() / 60.0  # difference (in minute) by now
                if (
                    middle_time_difference >= 0 and middle_time_difference <= 2
                ):  # If the train is halfway (for the user trip)
                    try:
                        if "Error" in requestedTrain:
                            msg = requestedTrain
                    except:
                        msg = (
                            requestedTrain.middleMsg()
                        )  # if its all ok i call the method of the Train object for create the message for departing trains

                    try:
                        keyboard = alertMenuButtons(requestedTrain.number)
                        bot.sendMessage(
                            row["user_id"],
                            emojize("%s" % (msg), use_aliases=True),
                            parse_mode="html",
                            disable_web_page_preview=True,
                            disable_notification=None,
                            reply_markup=keyboard,
                        )
                    except Exception as e:
                        # TODO: da gestire se son bloccato, anche il telegram.py devo gestire questa cosa, RICORDARSI
                        # if('blocked' in e):
                        pass
                print(start_time_difference)  # debug stuff to remove
                print(
                    middle_time_difference
                )  # Se non e running questa print non e aggiornata

        print(row["train_number"])
        print("\n")

    database.close()


if __name__ == "__main__":
    run()
