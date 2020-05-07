"""
A module that use API to retrive various types of stats about train in backend
"""
import requests
import json
import os
import datetime

from .buttons import *


def train_ranking_readable():
    """
    Function that return the train ranking in a readable mode for the user

    Returns:
        String with the train ranking
        Inlinekeybord Object for back at the primary menu
    """
    backend = os.environ.get("HOST_BACKEND", "backend")
    ranking = requests.get(f"http://{backend}:5000/api/stats/ranking")
    if ranking.status_code != 200:
        return "Impossibile visualizzare la classifica, riprova piú tardi!"

    ranking = ranking.json()

    ranking_best = ranking["best"][:4]
    ranking_worst = ranking["worst"][:4]

    msg = "<i>Treno -> ritardo medio</i>\n\n"
    msg += "<b>Treni Migliori:\n</b>"

    for i, _ in enumerate(ranking_best):
        msg += f"{str(i+1)}) "
        msg += str(ranking_best[i]["trainID"])
        msg += " -> "
        msg += ranking_best[i]["delay"].split(".")[0]
        msg += " min\n"

    msg += "<b>\nTreni Peggiori:\n</b>"

    for i, _ in enumerate(ranking_worst):
        msg += f"{str(i+1)}) "
        msg += str(ranking_worst[i]["trainID"])
        msg += " -> "
        msg += ranking_worst[i]["delay"].split(".")[0]
        msg += " min\n"

    return msg


"""
{'created': False, 'stats': [{'alert': '', 'arrival_datetime': '10:48:00', 'date': '2020-05-06', 'delay': -2,
'departure_datetime': '10:08:00', 'destination': 'LECCO', 'duration': 40, 'last_detection_datetime': '2020-05-06 10:46:30',
'last_detection_station': 'LECCO', 'number': 'S01529', 'origin': 'BERGAMO', 'real_arrival_datetime': '10:48:00',
'real_departure_datetime': '10:06:00', 'state': 'ON_TIME', 'trainID': 5038}]}
"""


def view_stat_util(train_code: int, nDays: int) -> str:
    """
    Function which contains the logic of the viewStatistics function

    Args:
        train_code: code of the entered train.
        nDays: number of days used to filter the results

    Returns:
        A message containing some interesting train statistic.
    """
    backend = os.environ.get("HOST_BACKEND", "backend")
    parsed_json = requests.get(
        f"http://{backend}:5000/api/train/{train_code}/stats?days={nDays}"
    )

    if parsed_json.status_code == 500 or parsed_json.status_code == 404:
        return (
            parsed_json.text + ":pensive:",
            "",
        )
    elif parsed_json.status_code != 200:
        raise Exception("Something wrong with the backend!")

    parsed_json = parsed_json.json()
    stats = parsed_json.get("stats")
    created = parsed_json.get("created", False)
    if created:
        raise Exception("Something wrong with the backend!")

    return_msg = f"Non sono disponilibi statistiche negli ultimi {nDays}gg :pensive:"
    daysMonitoring = len(stats)
    if daysMonitoring > 0:
        firstMonitoring = stats[0]["date"]
        lastMonitoring = stats[-1]["date"]
        sum_delay = onTimeDays = lateDays = nCancelled = nAltered = 0
        for stat in stats:
            sum_delay = sum_delay + stat["delay"]
            if stat["delay"] <= 0:
                onTimeDays = onTimeDays + 1
            else:
                lateDays = lateDays + 1
            if stat["state"] == "CANCELED":
                nCancelled = nCancelled + 1
            elif stat["state"] == "MODIFIED":
                nAltered = nAltered + 1
        averageDelay = sum_delay / daysMonitoring

        return_msg = f"Numero corse monitorate: {daysMonitoring}"
        return_msg += f"\nData primo monitoraggio: {datetime.datetime.strptime(firstMonitoring, '%d-%m-%Y')}"
        return_msg += f"\nData ultimo monitoraggio: {datetime.datetime.strptime(lastMonitoring, '%d-%m-%Y')}"
        return_msg += f"\nRitardo medio: {averageDelay}"
        return_msg += f"\nCorse in orario: {onTimeDays}"
        return_msg += f"\nCorse in ritardo: {lateDays}"
        return_msg += f"\nCorse cancellate: {nCancelled}"
        return_msg += f"\nnCorse alterate: {nAltered}"

    return return_msg


def viewStatistics(train_code: int) -> tuple:
    """
    Function to show some statistic for the entered train.

    Args:
        train_code: code of the entered train.

    Returns:
        A message bot containing some interesting train statistic.
    """
    day_dict = {30: "", 120: ""}
    for day in day_dict.keys():
        day_dict[day] = view_stat_util(train_code, day)

    bot_msg = f"📊 <b>Statistiche treno {train_code}</b>\n\n"
    bot_msg += "<b>STATISTICHE ultimi 30 giorni</b>\n"
    bot_msg += day_dict[30]
    bot_msg += "\n\n---------------------------------------------------------\n"
    bot_msg += "\n<b>STATISTICHE ultimi 120 giorni</b>\n"
    bot_msg += day_dict[120]
    bot_msg += "\n\n⚠️ Questi dati possono non essere affidabili, sono solo a scopo indicativo.\nSe vuoi maggiori indicazioni premi 'Statistiche Dettagliate'"

    return (bot_msg, rankingButtons())
