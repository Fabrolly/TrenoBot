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


def is_train_in_database(train_number):
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM backend_trains WHERE trainID = {train_number}")
    records = cursor.fetchall()
    return len(records) > 0


def store_train(train: dict):
    database = db_connection()
    train_id = train["fermate"][0]["id"]
    train_number = train["numeroTreno"]
    train_origin = train["origineZero"]
    train_destination = train["destinazioneZero"]
    train_stations = json.dumps(train["fermate"])
    train_departure_time = train["compOrarioPartenza"]
    train_arrival_time = train["compOrarioArrivo"]

    factors = (60, 1, 1 / 60)
    t1 = sum(i * j for i, j in zip(map(int, train["compDurata"].split(":")), factors))
    train_duration = t1

    cursor = database.cursor(prepared=True)
    insert_query = "INSERT INTO backend_trains (trainID, number, origin, destination, stations, departure_datetime, arrival_datetime, duration) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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
    except Exception as exception:
        raise exception


def get_stats(train_id):
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    query = f"SELECT backend_journeys.*, number, origin, destination,departure_datetime, arrival_datetime, duration,  stations FROM backend_journeys LEFT OUTER JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID WHERE backend_journeys.trainID={train_id} ORDER BY backend_journeys.DATE DESC"
    cursor.execute(query)
    stats = cursor.fetchall()
    return stats
