import datetime
import time
import requests
import json
import os

# import telepot
from emoji import emojize
from .buttons import *
from .bot_utility import create_bot


bot = create_bot()


def trip_search(command, arrivo, partenza, mese, giorno, ora, data, now, chat_id):
    # Chiedo alle api il trip
    backend = os.environ.get("HOST_BACKEND", "backend")
    parsed_json = requests.get(
        f"http://{backend}:5000/api/trip/search?from=%s&to=%s&date=%s-%s-%sT%s:00"
        % (partenza, arrivo, now.year, mese, giorno, ora)
    )
    if parsed_json.status_code == 500 or parsed_json.status_code == 404:

        return (
            parsed_json.text,
            backTripSearch(),
        )

    parsed_json = parsed_json.json()
    response_list = []
    keyboard_list = []
    try:
        for sol in range(0, 2):  # visualizzare le prime 2 opzioni
            risp = ""
            trains = []
            departure_time_keyboard = []
            arrival_time_keyboard = []
            departure = []
            arrival = []
            for cont in range(
                0, len(parsed_json["soluzioni"][sol]["vehicles"])
            ):  # ciclo che crea il messaggio per quando la soluzione ha piu treni
                departure_time = parsed_json["soluzioni"][sol]["vehicles"][cont][
                    "orarioPartenza"
                ]
                departure_day = departure_time[
                    departure_time.index("T") - 2 : departure_time.index("T")
                ]
                departure_month = departure_time[departure_time.index("-") + 1 :]
                departure_month = departure_month[: departure_time.index("-") - 2]
                departure_time = departure_time[
                    departure_time.index("T") + 1 : departure_time.index("T") + 6
                ]
                arrival_time = parsed_json["soluzioni"][sol]["vehicles"][cont][
                    "orarioArrivo"
                ]
                arrival_time = arrival_time[
                    arrival_time.index("T") + 1 : arrival_time.index("T") + 6
                ]

                # keyboard generate
                trains.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["numeroTreno"]
                )
                departure.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["origine"]
                )
                arrival.append(
                    parsed_json["soluzioni"][sol]["vehicles"][cont]["destinazione"]
                )
                departure_time_keyboard.append(departure_time)
                arrival_time_keyboard.append(arrival_time)

                # appendo i vari treni della soluzione in coda al messaggio di risposta
                risp += (
                    ":train2: Treno %s %s\n:arrow_right: <b>%s</b> da %s\n:arrow_left: <b>%s</b> a %s\n\n"
                    % (
                        parsed_json["soluzioni"][sol]["vehicles"][cont][
                            "categoriaDescrizione"
                        ],
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["numeroTreno"],
                        departure_time,
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["origine"],
                        arrival_time,
                        parsed_json["soluzioni"][sol]["vehicles"][cont]["destinazione"],
                    )
                )
            response = risp = (
                ":white_check_mark:<b>Soluzione %s</b>\n\n:calendar: %s-%s-%s\n:clock10:Durata <b>%s</b>\n\n%s"
                % (
                    sol + 1,
                    departure_day,
                    departure_month,
                    now.year,
                    parsed_json["soluzioni"][sol]["durata"],
                    risp,
                )
            )
            keyboard = searchResultMenuButtons(
                chat_id,
                trains,
                departure_time_keyboard,
                arrival_time_keyboard,
                departure,
                arrival,
            )
            response_list.append(response)
            keyboard_list.append(keyboard)
    except Exception as e:
        print(e)
        keyboard = backMainMenuButtons()
        return (
            "Le API di viaggiotreno non sono in grado di rispondere a questa richeiesta anche se il tuo comando e' valido.\n\nIl motivo e' sconosciuto e da attributire a viaggiatreno.it\n\nCerca qui il tuo treno: http://www.trenitalia.com/ \n\nQuando sai il numero del tuo treno torna qui!",
            keyboard,
        )

    return (response_list, keyboard_list)


def date_parser(command):

    now = datetime.datetime.now()

    output = ""

    if "-" not in command and "/" not in command:
        output = "%s-%s" % (command, now.month)
    else:
        if "/" in command:
            output = command.replace("/", "-")
        else:
            output = command

    if command == "":
        output = "%s-%s" % (now.day, now.month)

    return output
