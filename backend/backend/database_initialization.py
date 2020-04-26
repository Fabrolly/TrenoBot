"""
A module to initialize the database and the necessary tables
"""
import os

import MySQLdb
import warnings

warnings.filterwarnings("ignore", category=MySQLdb.Warning)


def database_initialization(server: str, user: str, password: str):
    """
    Create the database for the backend

    Args:
        server: host of the databsase
        user: user of the databsase
        password: password of the databsase
    """
    # Connecting to database as root
    # database = MySQLdb.connect("localhost","root", loginInfo.databasePWS())
    database = MySQLdb.connect(server, user, password)
    cursor = database.cursor()

    # If the TRENOBOT database doses not exist, create and open it (if already exist a warning will be generated)
    cursor.execute("CREATE DATABASE IF NOT EXISTS TRENOBOT;")
    cursor.execute("use TRENOBOT;")

    # If tables doses not exist, create it (if already exist a warning will be generated)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS backend_trains (trainID INT PRIMARY KEY, number TEXT, origin TEXT, destination TEXT, stations JSON, departure_datetime TIME, arrival_datetime TIME, duration INT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS backend_journeys (date DATE, trainID INT, real_departure_datetime TIME, real_arrival_datetime TIME, delay INT, state TEXT, alert TEXT, last_detection_datetime DATETIME, last_detection_station TEXT, PRIMARY KEY(date, trainID))"
    )

    database.commit()

    # Disconnecting
    database.close()
