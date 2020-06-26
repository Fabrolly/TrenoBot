"""
A module to initialize the database and the necessary tables
"""
import os

import MySQLdb
import warnings

warnings.filterwarnings("ignore", category=MySQLdb.Warning)


def database_initialization(server: str, user: str, password: str, seed=False):
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

    if seed:
        cursor.execute("DELETE FROM backend_journeys WHERE 1")
        cursor.execute("DELETE FROM backend_trains WHERE 1")
        cursor.execute(
            "INSERT INTO backend_trains VALUES (1, 1, 'Milano', 'Bergamo', NULL, NULL, NULL, NULL)"
        )
        cursor.execute(
            "INSERT INTO backend_journeys VALUES ('2020-05-10', 1, NULL, NULL, 10, 'DELAY', NULL, NULL, NULL)"
        )
        cursor.execute(
            "INSERT INTO backend_journeys VALUES ('2020-05-11', 1, NULL, NULL, 1, 'DELAY', NULL, NULL, NULL)"
        )
        cursor.execute(
            "INSERT INTO backend_journeys VALUES ('2020-05-12', 1, NULL, NULL, -1, 'DELAY', NULL, NULL, NULL)"
        )
        cursor.execute(
            "INSERT INTO backend_journeys VALUES ('2020-05-13', 1, NULL, NULL, -3, 'DELAY', NULL, NULL, NULL)"
        )
        cursor.execute(
            "INSERT INTO backend_journeys VALUES ('2020-05-14', 1, NULL, NULL, -5, 'DELAY', NULL, NULL, NULL)"
        )

    database.commit()

    # Disconnecting
    database.close()
