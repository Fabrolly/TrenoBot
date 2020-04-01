# This class initialize the database and the necessary tables
# For more information about DB see: /Documentation/Infrastructure and technologies.md
import sys

import MySQLdb
import warnings

warnings.filterwarnings("ignore", category=MySQLdb.Warning)
# ♦import loginInfo


def database_initialization(server, user, password):
    # Connecting to database as root
    # database = MySQLdb.connect("localhost","root", loginInfo.databasePWS())
    database = MySQLdb.connect(server, user, password)
    cursor = database.cursor()

    # If the TRENOBOT database doses not exist, create and open it (if already exist a warning will be generated)
    cursor.execute("CREATE DATABASE IF NOT EXISTS TRAINSTATISTICS;")
    cursor.execute("use TRAINSTATISTICS;")

    # If tables doses not exist, create it (if already exist a warning will be generated)
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS trains (trainID INT PRIMARY KEY, number TEXT, origin TEXT, destination TEXT, stations JSON, departure_datetime DATETIME, arrival_datetime DATETIME, duration INT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS journeys (date DATETIME, trainID INT, real_departure_datetime DATETIME, real_arrival_datetime DATETIME, delay INT, state TEXT, alert TEXT, last_detection_datetime DATETIME, last_detection_station TEXT, last_update DATETIME, final_status TEXT, final_delay INT, PRIMARY KEY(date, trainID))"
    )

    database.commit()

    # Disconnecting
    database.close()


# launch unit test cases
if __name__ == "__main__":

    if not len(sys.argv) == 4:
        print(
            "Il comando necessita in input dei parametri per il server, utente e password"
        )
        exit()

    server = sys.argv[1]
    user = sys.argv[2]
    password = sys.argv[3]

    database_initialization(server, user, password)
