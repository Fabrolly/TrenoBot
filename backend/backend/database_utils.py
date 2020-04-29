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
    train_stations = train["fermate"]
    train_departure_time = train["compOrarioPartenza"]
    train_arrival_time = train["compOrarioArrivo"]


    #Il campo stazioni lo memorizzo nel DB dei treni controllati a livello di statistiche poiché puo essere utile elenco stazioni
    #Visto che questo campo contiene un sacco di info real time inutili, che non memorizzo del DB quindi li cancello
    for item in train_stations:    
        item.pop('actualFermataType', None)
        item.pop('arrivoReale', None)
        item.pop('binarioEffettivoArrivoCodice', None)
        item.pop('binarioEffettivoArrivoDescrizione', None)
        item.pop('binarioEffettivoArrivoTipo', None)
        item.pop('binarioEffettivoPartenzaCodice', None)
        item.pop('binarioEffettivoPartenzaDescrizione', None)
        item.pop('binarioEffettivoPartenzaTipo', None)
        item.pop('binarioProgrammatoArrivoDescrizione', None)
        item.pop('binarioProgrammatoPartenzaCodice', None)
        item.pop('binarioProgrammatoPartenzaDescrizione', None)
        item.pop('effettiva', None)
        item.pop('isNextChanged', None)
        item.pop('kcNumTreno', None)
        item.pop('listaCorrispondenze', None)
        item.pop('materiale_label', None)
        item.pop('orientamento', None)
        item.pop('partenzaReale', None)
        item.pop('partenzaTeoricaZero', None)
        item.pop('programmataZero', None)
        item.pop('ritardo', None)
        item.pop('ritardoArrivo', None)
        item.pop('ritardoPartenza', None)
        item.pop('visualizzaPrevista', None)
        item.pop('arrivoTeoricoZero', None)
        item.pop('binarioProgrammatoArrivoCodice', None)
        item.pop('nextTrattaType', None)
        item.pop('programmata', None)

    train_stations = json.dumps(train_stations)

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
    query = f"SELECT backend_journeys.*, number, origin, destination,departure_datetime, arrival_datetime, duration FROM backend_journeys LEFT OUTER JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID WHERE backend_journeys.trainID={train_id} ORDER BY backend_journeys.DATE DESC"
    cursor.execute(query)
    stats = cursor.fetchall()
    return stats


def get_best_trains():
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    query = f"SELECT backend_trains.trainID, AVG(delay) as delay FROM backend_journeys JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID GROUP BY backend_trains.trainID ORDER BY AVG(delay) ASC LIMIT 10"
    cursor.execute(query)
    best_trains = cursor.fetchall()
    return best_trains


def get_worst_trains():
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    query = f"SELECT backend_trains.trainID, AVG(delay) as delay FROM backend_journeys JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID GROUP BY backend_trains.trainID ORDER BY AVG(delay) DESC LIMIT 10"
    cursor.execute(query)
    worst_trains = cursor.fetchall()
    return worst_trains


def get_general_stats():
    database = db_connection()
    cursor = database.cursor(dictionary=True)
    query = f"SELECT AVG(delay) as avg_delay FROM backend_journeys JOIN backend_trains ON backend_journeys.trainID=backend_trains.trainID"
    cursor.execute(query)
    stats = cursor.fetchall()[0]
    return stats
