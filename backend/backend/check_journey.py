"""
Module that define functionalities for checking registered trains for cancellations, delays or changes.
"""
import sys
import os
import requests
from datetime import datetime, timedelta
import datetime as dt
import mysql.connector
from mysql.connector import Error
import json
import typing


def db_connection():
    """
    Return a connection to the database

    Returns:
        connection to the database
    """
    server = os.environ.get("DATABASE_HOST")
    user = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    database = mysql.connector.connect(
        host=server, database="TRENOBOT", user=user, password=password
    )
    return database


def convert_timestamp(timestamp: typing.Optional[float]) -> typing.Optional[str]:
    """
    Format a timestamp to string

    Args:
        timestamp: the timestamp to format

    Returns:
        the timestamp formatted as "%Y-%m-%d %H-%M-%S"
    """
    if timestamp == None:
        return None
    else:
        datetime = dt.datetime.fromtimestamp(timestamp / 1000)
        return datetime.strftime("%Y-%m-%d %H:%M:%S")


def add_journey_db(trainID: int):
    """
    Update the stored status of a certain train in the database

    Args:
        trainID: train identifier
    """
    database = db_connection()
    cursor = database.cursor(buffered=True)

    train_response = requests.get("http://backend:5000/api/train/%s" % trainID)

    if train_response.status_code != 200:
        return "Treno non esistente?"
    else:
        train = train_response.json()
        now = datetime.now()

        if "PG" in train["tipoTreno"]:
            state = "ON_TIME"
        else:
            if "ST" in train["tipoTreno"]:
                state = "CANCELED"
            else:
                state = "MODIFIED"

        if (
            "ON_TIME" in state
            and train["stazioneUltimoRilevamento"] == train["destinazione"]
        ):
            # se é regolare ma non é ancora arrivato non aggiorno il viaggio (é in grande ritardo)
            train_departure_time = train["compOrarioPartenzaZeroEffettivo"]
            train_arrival_time = train["compOrarioArrivoZeroEffettivo"]
            train_delay = train["ritardo"]
            train_state = state
            train_alert = train["subTitle"]
            train_last_detection_time = convert_timestamp(train["oraUltimoRilevamento"])
            train_last_detection_station = train["stazioneUltimoRilevamento"]

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
    """
    Check the status of trains that should have arrived in the last 20 minutes
    """
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
