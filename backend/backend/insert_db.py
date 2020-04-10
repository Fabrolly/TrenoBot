import sys
import os
import requests
import datetime as dt
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import json
from .check_journey import add_journey_db


def db_connection():
    server = os.environ.get("DATABASE_HOST")
    user = os.environ.get("DATABASE_USER")
    password = os.environ.get("DATABASE_PASSWORD")
    database = mysql.connector.connect(
        host=server, database="TRENOBOT", user=user, password=password
    )
    return database


def check_existing(number):
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM backend_trains")
    records = cursor.fetchall()

    for row in records:
        if row["trainID"] == number:
            return True
    return False


def add_to_db(json_train):
    database = db_connection()
    train_id = json_train["fermate"][0]["id"]
    train_number = json_train["numeroTreno"]
    train_origin = json_train["origineZero"]
    train_destination = json_train["destinazioneZero"]
    train_stations = json.dumps(json_train["fermate"])
    train_departure_time = json_train["compOrarioPartenza"]
    train_arrival_time = json_train["compOrarioArrivo"]

    factors = (60, 1, 1 / 60)
    t1 = sum(
        i * j for i, j in zip(map(int, json_train["compDurata"].split(":")), factors)
    )
    train_duration = t1

    cursor = database.cursor(prepared=True)
    insert_query = """ INSERT INTO backend_trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    insert_tuple = (
        train_number,
        train_id,
        train_origin,
        train_destination,
        train_stations,
        train_departure_time,
        train_arrival_time,
        train_duration,
    )

    try:
        cursor.execute(insert_query, insert_tuple)
        database.commit()
    except Exception as e:
        return e
    return True


def stats_json_fetch(trainID):
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    query = (
        "SELECT backend_journeys.*, number, origin, destination,departure_datetime, arrival_datetime, duration,  stations FROM backend_journeys LEFT OUTER JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID WHERE backend_journeys.trainID=%s ORDER BY backend_journeys.DATE DESC"
        % (trainID)
    )
    cursor.execute(query)
    json_string = json.dumps(cursor.fetchall(), indent=4, sort_keys=True, default=str)

    return json_string


def add_train(number):
    if check_existing(number):
        return stats_json_fetch(number)
    else:
        json_train = requests.get("http://backend:5000/api/train/%s" % number)
        if json_train.status_code != 200:
            return (
                "Train Not Found",
                404,
            )  # se il treno non esiste ritorno l'errore che le api mi danno
        else:
            json_train = json_train.json()
            res = add_to_db(json_train)
            if res:
                return stats_json_fetch(number) #avendolo appena aggiunto ritorneró un array vuoto 
            else:
                return str(res), 404
