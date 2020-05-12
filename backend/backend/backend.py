"""
The entrypoint/main for the backend service, defining routes and the background thread to check trains.
"""
from flask import Flask, request, jsonify, abort
import flask

import requests
import datetime
import os
import threading
import pathlib
import time


from .database_initialization import database_initialization
from . import database_utils
from . import check_journey
from . import trenitalia_interface

app = Flask(__name__)


@app.route("/api/train/<int:train_number>", methods=["GET"])
def get_train_status(train_number: int):
    """
    .. :quickref: Train; Get all the real time information for a train


    Get all the real time information for a train

    Returns:
        a JSON with the data

    Args:
        train_number: the identifier of the train
    """

    # find station ID for the full request
    station_id = trenitalia_interface.find_station_id(train_number)
    if station_id is None:
        return "Train not found", 404

    try:
        return jsonify(trenitalia_interface.train_status(station_id, train_number))
    except:
        return "Internal Server Error", 500


@app.route("/api/trip/search")
def trip_search():
    """
    .. :quickref: Trip; Search for a trip

    Given a "from", "to", and "date" as query parameters, search for trips solutions

    Returns:
        a JSON with the data
    """
    # prendo in input gli argomenti della ricerca e verifico che ci siano tutti e che siano corretti
    partenza = request.args.get("from")
    arrivo = request.args.get("to")
    data = request.args.get("date")
    if None in [partenza, arrivo, data]:
        return "A parameter is missing", 500

    try:
        datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
    except Exception:
        return "Data format is wrong. Use YYYY-MM-GGTHH:MM:SS", 500

    # Creo url per la richiesta del CODICE DELLE STAZIONI e interrogo
    url_partenza = f"http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/{partenza}"
    url_arrivo = f"http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/{arrivo}"

    # Interrogo per ottenere il codice della stazione di PARTENZA
    risposta_stazione_partenza = requests.get(url_partenza).text
    if len(risposta_stazione_partenza) == 0:
        return "Departure station not existing", 404

    codice_stazione_partenza = risposta_stazione_partenza.split("\n")[0].split("|")[1]
    while codice_stazione_partenza[0] == "S":
        codice_stazione_partenza = codice_stazione_partenza[1:]

    # Interrogo per ottenere il codice della stazione di ARRIVO
    risposta_stazione_arrivo = requests.get(url_arrivo).text
    if len(risposta_stazione_arrivo) == 0:
        return "Destination station not existing", 404

    codice_stazione_arrivo = risposta_stazione_arrivo.split("\n")[0].split("|")[1]
    while codice_stazione_arrivo[0] == "S":
        codice_stazione_arrivo = codice_stazione_arrivo[1:]

    # Interrogo con codici delle stazioni di partenza e ritorno e data e ora CODICEPARTENZA/CODICEARRIVO/AAAA-MM-GGTHH:MM:SS occhio alla T che separa data e ora
    url_ricerca = f"http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/{codice_stazione_partenza}/{codice_stazione_arrivo}/{data}"
    try:
        response_ricerca = requests.get(url_ricerca)
        response_ricerca.json()
    except Exception:
        return "Internal server error", 500

    return jsonify(response_ricerca.json())


@app.route("/api/train/<int:train_number>/stats", methods=["GET"])
def get_stats(train_number: int):

    """
    .. :quickref: Stats; Get historical stats for a train

    Get historical stats for a train

    Returns:
        a JSON with the data

    Args:
        train_number: the identifier of the train
    """
    if database_utils.is_train_in_database(train_number):
        return jsonify(
            {"created": False, "stats": database_utils.get_stats(train_number)}
        )
    else:
        # register the train
        try:
            station_id = trenitalia_interface.find_station_id(train_number)
            train = trenitalia_interface.train_status(station_id, train_number)
        except Exception:
            return "Train not found", 404

        try:
            database_utils.store_train(train)
        except Exception:
            return "Internal server error", 500

        return jsonify({"created": True, "stats": []})


@app.route("/api/stats/ranking", methods=["GET"])
def get_stats_ranking():
    """
    .. :quickref: Ranking; Get ranking for all the trains


    Get ranking for all the trains

    Returns:
        a JSON with the data
    """
    best_trains = database_utils.get_best_trains()
    for train in best_trains:
        train["stations"] = train["stations"].replace('"', "'").replace("null", "None")
        train["stations"] = (
            train["stations"].replace("false", "False").replace("true", "True")
        )
        train["stations"] = eval(train["stations"])
    best_trains = [
        {
            "trainID": train["trainID"],
            "delay": train["delay"],
            "reliabilityIndex": train["delay"]
            / train["duration"]
            / len(train["stations"])
            * -1000,
        }
        for train in best_trains
    ]
    best_trains = sorted(best_trains, key=lambda d: d["reliabilityIndex"], reverse=True)
    worst_trains = database_utils.get_worst_trains()
    for train in worst_trains:
        train["stations"] = train["stations"].replace('"', "'").replace("null", "None")
        train["stations"] = (
            train["stations"].replace("false", "False").replace("true", "True")
        )
        train["stations"] = eval(train["stations"])
    worst_trains = [
        {
            "trainID": train["trainID"],
            "delay": train["delay"],
            "reliabilityIndex": train["delay"]
            / train["duration"]
            / len(train["stations"])
            * -1000,
        }
        for train in worst_trains
    ]
    worst_trains = sorted(worst_trains, key=lambda d: d["reliabilityIndex"])
    return jsonify({"best": best_trains, "worst": worst_trains})


@app.route("/api/stats/general", methods=["GET"])
def get_general_stats():
    """
    .. :quickref: GeneralStats; Get general aggregated stats

    Get general aggregated stats

    Returns:
        a JSON with the data
    """
    stats = database_utils.get_general_stats()
    return jsonify(stats)


def check_arrival_loop():
    """
    Run the periodic checks for trains
    """
    while True:
        check_journey.check_arrival()
        print("Controllo automatico treni in arrivo eseguito. Prossimo tra 10 minuti.")
        time.sleep(10 * 60)  # sleep 10 minutes


class JSONEncoderWithDefault(flask.json.JSONEncoder):
    """
    Override some of the the standard Flask JSON Encoder behaviors
    """

    def default(self, o):
        """
        When serialization to JSON is not available, return everything as a string.

        This is useful to handle objects such as datetimes.
        """
        return str(o)


if __name__ == "__main__":
    SERVER = os.environ.get("DATABASE_HOST")
    USER = os.environ.get("DATABASE_USER")
    PASSWORD = os.environ.get("DATABASE_PASSWORD")
    database_initialization(SERVER, USER, PASSWORD)

    x = threading.Thread(target=check_arrival_loop)
    x.start()

    app.json_encoder = JSONEncoderWithDefault
    app.run(debug=True, host="0.0.0.0")
