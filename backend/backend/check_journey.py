import sys
import os
import requests
from datetime import datetime, timedelta
import mysql.connector
from mysql.connector import Error
import json

def db_connection():
    server = os.environ.get("DATABASE_HOST")
    user = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    database = mysql.connector.connect(
        host=server, database="TRENOBOT", user=user, password=password
    )
    return database


def add_journey_db(trainID):
    database = db_connection()
    cursor2 = database.cursor(buffered=True)

    json_train = requests.get("http://backend:5000/api/train/%s" % trainID)

    if json_train.status_code != 200:
        return  # non riesco ad aggiornare il treno!
    else:
        now = datetime.now()

        json_train = json_train.json()
        train_departure_time = json_train["compOrarioArrivoZeroEffettivo"]
        train_arrival_time = json_train["compOrarioPartenzaZeroEffettivo"]
        train_delay = json_train["ritardo"]
        train_state = json_train["statoTreno"]
        train_alert = json_train["subTitle"]
        train_last_detection_time = json_train["oraUltimoRilevamento"]
        train_last_detection_station = json_train["stazioneUltimoRilevamento"]

        insert_query = """ INSERT INTO backend_journeys (date, trainID, real_departure_datetime, real_arrival_datetime, delay, state, alert, last_detection_datetime, last_detection_station) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        insert_tuple = (
            now.strftime("%Y-%m-%d"),
            trainID,
            train_departure_time,
            train_arrival_time,
            train_delay,
            train_state,
            train_alert,
            train_last_detection_time,
            train_last_detection_station,
        )
        cursor2.execute(insert_query, insert_tuple)
        database.commit()


def check_arrival():
    database = db_connection()
    cursor = database.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM backend_trains")
    trains = cursor.fetchall()

    now = datetime.now()

    msg = ""
    for row in trains:
        now_datetime = timedelta(hours=now.hour, minutes=now.minute, seconds=0)
        minute_difference = (
            now_datetime - row["arrival_datetime"]
        ).total_seconds() / 60.0

        if minute_difference > 15:
            now = datetime.now()
            cursor.execute("SELECT * FROM backend_journeys")
            trains_j = cursor.fetchall()

            for row_j in trains_j:
                if row_j["trainID"] == row["trainID"]:
                    if row_j["date"] != now.date():
                        add_journey_db(row["trainID"])
                        msg += "aggiornato il treno %s" % row["trainID"]
                    else:
                        msg += "il treno %s é giá aggiornato" % row["trainID"]

        else:
            msg += "il treno %s non é ancora arrivato" % row["trainID"]

    return msg
