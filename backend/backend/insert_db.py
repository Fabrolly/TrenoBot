import sys
import os
import requests
import datetime as dt
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import json

server = os.environ.get("DATABASE_HOST")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
database = mysql.connector.connect(
    host=server, database="TRENOBOT", user=user, password=password
)


def check_existing(number):
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM backend_trains")
    records = cursor.fetchall()

    for row in records:
        print(row)
        if row["trainID"] == number:
            return True
        else:
            return False


def convert_timestamp(timestamp):
    datetime = dt.datetime.fromtimestamp(timestamp / 1000)
    return datetime.strftime("%Y-%m-%d %H:%M:%S")


def add_to_db(json_train):
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

    cursor.execute(insert_query, insert_tuple)
    database.commit()


def add_train(number):
    if check_existing(number):
        return "il treno é nel db!"  # TODO: devo ritornarci le statistiche!
    else:
        json_train = requests.get("http://backend:5000/api/train/%s" % number)
        if json_train.status_code != 200:
            return (
                "Train Not Found",
                404,
            )  # se il treno non esiste ritorno l'errore che le api mi danno
        else:
            json_train = json_train.json()
            add_to_db(json_train)
            return "[]"  # ho aggiunto il treno al db ma non ho ancora le statistiche
