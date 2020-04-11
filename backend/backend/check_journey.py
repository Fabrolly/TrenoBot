import sys
import os
import requests
from datetime import datetime, timedelta
import datetime as dt
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


def convert_timestamp(timestamp):
    if timestamp == None:
        return None
    else:
        datetime = dt.datetime.fromtimestamp(timestamp / 1000)
        return datetime.strftime("%Y-%m-%d %H:%M:%S")


def add_journey_db(trainID):
    database = db_connection()
    cursor = database.cursor(buffered=True)

    json_train = requests.get("http://backend:5000/api/train/%s" % trainID)

    if json_train.status_code != 200:
        return "Treno non esistente?"
    else:
        json_train = json_train.json()
        now = datetime.now()

        if "PG" in json_train["tipoTreno"]:
            state = "Regolare"
        else:
            if "ST" in json_train["tipoTreno"]:
                state = "Soppresso"
            else:
                state = "Parzialmente Soppresso"

        if (
            "Regolare" in state
            and json_train["stazioneUltimoRilevamento"] == json_train["destinazione"]
        ):
            # se é regolare ma non é ancora arrivato non aggiorno il viaggio (é in grande ritardo)
            train_departure_time = json_train["compOrarioPartenzaZeroEffettivo"]
            train_arrival_time = json_train["compOrarioArrivoZeroEffettivo"]
            train_delay = json_train["ritardo"]
            train_state = state
            train_alert = json_train["subTitle"]
            train_last_detection_time = convert_timestamp(
                json_train["oraUltimoRilevamento"]
            )
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
        else:
            print(
                "Il treno %s dovrebbe essere arrivato ma non é a destinazione! Journey non aggiunta. Riprovo al prossimo controllo"
                % (trainID)
            )

        try:
            cursor.execute(insert_query, insert_tuple)
            database.commit()
            print("Journey odierna del treno %s aggiunta con successo" % (trainID))
        except Exception as e:
            return e
        return True


def check_arrival():
    database = db_connection()
    cursor = database.cursor(dictionary=True, buffered=True)
    cursor.execute("SELECT * FROM backend_trains")
    trains = cursor.fetchall()

    now = datetime.now()
    for row in trains:
        # per ogni treno nel db controllo quando devono arrivare a destinazione in teoria
        now_datetime = timedelta(hours=now.hour, minutes=now.minute, seconds=0)
        minute_difference = (
            now_datetime - row["arrival_datetime"]
        ).total_seconds() / 60.0

        if minute_difference > 20:
            # Seleziono i treni che sono arrivati (in teoria) giá da almeno 20 minuti
            query = (
                "SELECT backend_journeys.DATE FROM backend_journeys INNER JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID WHERE backend_journeys.trainID=%s ORDER BY backend_journeys.DATE DESC"
                % (row["trainID"])
            )
            cursor.execute(query)
            last_update = cursor.fetchone()

            if last_update is None or last_update["DATE"] != now.date():
                # Devo aggiornare il viaggio odierno o l'ho giá aggiornato oggi? Controllo il valore di last_update
                res = add_journey_db(row["trainID"])  # lo aggiorno

                if not res:
                    # qualcosa é andato storto nell'aggiornamento!
                    return str(res)
