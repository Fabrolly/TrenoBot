from flask import Flask, request, jsonify, abort
import requests
import datetime
import os

from .database_initialization import database_initialization
from .insert_db import add_train

server = os.environ.get("DATABASE_HOST")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")

database_initialization(server, user, password)


app = Flask(__name__)

# request the Station_ID of the train by the number of the train.
# For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def find_station_id(train_number):
    try:
        response = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s"
            % train_number
        )
    except requests.ConnectionError:
        raise ConnectionError  # probably the trenitalia API are offline
    response.encoding = "utf-8"
    response = response.text
    if len(response) != 0 and "<H1>" not in response and response is not None:
        if (
            "-" in response
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response = response[(response.index("|") + 1) :]
            response = response[(response.index("-") + 1) : (response.index("\n"))]
            return response  # return the ID of the train
        else:
            raise TrainNotFoundException  # Il treno non esiste


# return the JSON containing all the real time information of a train, by it's number
@app.route("/api/train/<int:number>", methods=["GET"])
def realTimeInformation(number):
    station_id = find_station_id(number)  # I need also the Station_ID for the request
    if station_id is None:
        return abort(404)
    url = f"{station_id}/{number}"  # See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER
    try:
        raw_json = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/%s"
            % url
        )
        return jsonify(raw_json.json())
    except:
        return abort(500)  # trenitalia api offline


@app.route("/api/trip/search",)
def tripSearch():
    args = request.args
    if (
        request.args
    ):  # prendo in input gli argomenti della ricerca e verifico che ci siano tutti e che siano corretti
        if "from" in args:
            partenza = args["from"]
        else:
            return "No from string received", 500
        if "to" in args:
            arrivo = args.get("to")
        else:
            return "No to string received", 500
        if "date" in args:
            data = args["date"]
            try:
                datetime.datetime.strptime(data, "%Y-%m-%dT%H:%M:%S")
            except Exception as e:
                return "Data format is wrong. Use YYYY-MM-GGTHH:MM:SS", 500
        else:
            return "No date string received", 500
    else:
        return "No query string received", 500

    # Creo url per la richiesta del CODICE DELLE STAZIONI e interrogo
    url_partenza = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s"
        % partenza
    )
    url_arrivo = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/autocompletaStazione/%s"
        % arrivo
    )
    # Interrogo per ottenere il codice della stazione di PARTENZA
    codice_stazione_partenza = requests.get(url_partenza)
    codice_stazione_partenza = codice_stazione_partenza.text
    try:
        if "\n" in codice_stazione_partenza:
            codice_stazione_partenza = codice_stazione_partenza[
                codice_stazione_partenza.index("|")
                + 2 : codice_stazione_partenza.index("\n")
            ]
        else:
            codice_stazione_partenza = codice_stazione_partenza[
                codice_stazione_partenza.index("|") + 2 :
            ]

        while codice_stazione_partenza[0] == "0":
            codice_stazione_partenza = codice_stazione_partenza[1:]
    except Exception as e:
        return (
            "Departure station not existing",
            500,
        )  # stazione di partenza non esistente
    # Interrogo per ottenere il codice della stazione di ARRIVO
    codice_stazione_arrivo = requests.get(url_arrivo).text
    try:
        if "\n" in codice_stazione_arrivo:
            codice_stazione_arrivo = codice_stazione_arrivo[
                codice_stazione_arrivo.index("|")
                + 2 : codice_stazione_arrivo.index("\n")
            ]
        else:
            codice_stazione_arrivo = codice_stazione_arrivo[
                codice_stazione_arrivo.index("|") + 2 :
            ]
        while codice_stazione_arrivo[0] == "0":
            codice_stazione_arrivo = codice_stazione_arrivo[1:]
    except Exception as e:
        return (
            "Destination station not existing",
            500,
        )  # stazione di arrivo non esistente
    # Interrogo con codici delle stazioni di partenza e ritorno e data e ora CODICEPARTENZA/CODICEARRIVO/AAAA-MM-GGTHH:MM:SS occhio alla T che separa data e ora
    url_ricerca = (
        "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/soluzioniViaggioNew/%s/%s/%s"
        % (codice_stazione_partenza, codice_stazione_arrivo, data)
    )
    response_json = requests.get(url_ricerca)
    try:
        response_json.json()
    except Exception as e:
        return abort(500)

    return jsonify(response_json.json())


@app.route("/api/add_train/<int:number>", methods=["GET"])
def add_new_train_db(number):
    return add_train(number)


@app.route("/api/checkarrival", methods=["GET"])
def check():
    from .check_journey import check_arrival

    return check_arrival()


class TrainNotFoundException(Exception):
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
