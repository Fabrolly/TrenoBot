"""
A module to interact with the database
"""
import MySQLdb
import time
from datetime import datetime, timedelta
import datetime as dt
import requests
import typing
from .train import *
from .bot_utility import connect_db
import os

# import loginInfo


def createTrain(trainNumber):
    now = dt.datetime.now()

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE TRENOBOT;")

    # Search for the train number
    row = cursor.execute(
        "SELECT * FROM trains WHERE number = '%d'" % (int(trainNumber))
    )
    dbLine = cursor.fetchone()

    if (
        row == 1 and ((now - dbLine["last_update"]).total_seconds() / 60.0) < 1.5
    ):  # if the train is in DB and last update recent than 1,5 minutes (1:30 min)
        usedTrain = trainObjFromDb(dbLine)
    else:  # else, I must update/add the train in DB
        createdLine = addOrUpdateTrainDB(trainNumber)
        if "Error" in createdLine:
            database.close()
            return createdLine

        usedTrain = trainObjFromDb(createdLine)

    database.close()
    return usedTrain


def addOrUpdateTrainDB(number):

    backend = os.environ.get("HOST_BACKEND", "backend")
    jsonapi = requests.get(f"http://{backend}:5000/api/train/{number}")

    # Handle errors:
    if jsonapi.status_code == 404:
        return "Error: Il treno cercato non esiste :pensive:"
    if jsonapi.status_code == 500:
        return "Error: Le API di viaggiotreno sono offline, non riesco a comunicare! :pensive:"

    # Convert API response to JSON
    jsonapi = jsonapi.json()

    # Connecting to database
    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor()

    # Prepare name filed for INSERT record on DB
    field_train_db = """id, number, origin, destination, departure_datetime, arrival_datetime, duration, delay, state,
                        last_detection_time, last_detection_station, stations, alert, last_update"""

    # Prepare content filed that needing changes compared to the original json by viaggiotreno
    state = train_state(jsonapi)  # Deleted, regular..
    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )  # Actual time, for the last_update filed

    rawjson = str(jsonapi)
    rawjson = rawjson.replace("'", '"')
    rawjson = rawjson.replace("None", "null")
    rawjson = rawjson.replace("False", "false")
    rawjson = rawjson.replace("True", "true")

    try:
        fermate = rawjson[
            rawjson.index('"fermate":') + 10 : rawjson.index("}],") + 2
        ]  # list of all the stops, with binary and other info. I leave it in JSON.
    except:
        return "Le API di viaggiotreno non mi hanno restituito le fermate per questo treno. Riprova piú tardi o con un altro treno! :pensive:"

    # Prepare string for the content filed in INSERT record on DB
    content_filed1 = "'%s', %s, '%s', '%s', '%s', '%s', '%s'," % (
        jsonapi["fermate"][0]["id"],
        jsonapi["numeroTreno"],
        jsonapi["origineZero"],
        jsonapi["destinazioneZero"],
        convert_timestamp(jsonapi["orarioPartenza"]),
        convert_timestamp(jsonapi["orarioArrivo"]),
        jsonapi["compDurata"],
    )
    content_filed2 = "%s, '%s', '%s', '%s', '%s', '%s', '%s'" % (
        jsonapi["ritardo"],
        state,
        convert_timestamp(jsonapi["oraUltimoRilevamento"]),
        jsonapi["stazioneUltimoRilevamento"],
        fermate,
        jsonapi["subTitle"],
        now,
    )
    content_filed_db = "%s %s" % (content_filed1, content_filed2)

    # Insert the record into database "TRENOBOT", table "train"
    try:
        cursor.execute("USE TRENOBOT;")
        cursor.execute(
            "REPLACE INTO trains (%s) VALUES (%s);" % (field_train_db, content_filed_db)
        )  # Use REPLACE instead of INSERT for update old records if exists
        database.commit()
        database.close()
    except MySQLdb.Error as e:
        database.rollback()
        database.close()
        return "Got Error {!r}, errno is {}".format(e, e.args[0])

    database = connect_db()
    if isinstance(database, str):
        if "Connection Error" in database:
            exit()
    cursor = database.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("USE TRENOBOT;")
    cursor.execute("SELECT * FROM trains WHERE number = '%d'" % (int(number)))
    createdLine = cursor.fetchone()
    database.close()  # closing the db connection

    return createdLine


def convert_timestamp(timestamp: typing.Optional[float]) -> typing.Optional[str]:
    """
    Format a timestamp to string

    Args:
        timestamp: the timestamp to format

    Returns:
        the timestamp formatted as "%Y-%m-%d %H-%M-%S"
    """
    if timestamp is None:
        return "-"
    else:
        datetime = dt.datetime.fromtimestamp(timestamp / 1000)
        return datetime.strftime("%Y-%m-%d %H:%M:%S")


# Function to interpret the train status from the codes
def train_state(jsonapi: dict) -> str:
    """
    Get the train status from the status code

    Params:
        jsonapi: train instance

    Returns:
        a string representing the status of the train
    """
    if "PG" in jsonapi["tipoTreno"]:
        state = "Regolare"
    else:
        if "ST" in jsonapi["tipoTreno"]:
            state = "Soppresso :red_circle: :red_circle:"
        else:
            state = "Parzialmente Soppresso :red_circle:"
    return state


def trainObjFromDb(dbLine: dict) -> Train:
    """
    Initialize a train instance from a database row

    Params:
        dbLine: a row as a dict coming from the database

    Returns:
        a train object mapping the database row
    """
    usedTrain = Train(
        dbLine["id"],
        dbLine["number"],
        dbLine["origin"],
        dbLine["destination"],
        dbLine["departure_datetime"],
        dbLine["arrival_datetime"],
        dbLine["duration"],
        dbLine["delay"],
        dbLine["state"],
        dbLine["last_detection_time"],
        dbLine["last_detection_station"],
        dbLine["stations"],
        dbLine["alert"],
        dbLine["last_update"],
    )
    return usedTrain
