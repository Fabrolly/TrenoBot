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

    return_msg = f"Non sono disponibili statistiche negli ultimi {nDays} giorni :pensive:\nControlla di aver inserito il treno nella tua Lista!"
    daysMonitoring = len(stats)
    if daysMonitoring > 0:
        lastMonitoring = datetime.datetime.strptime(stats[-1]["date"], "%Y-%m-%d")
        sum_delay = nCancelled = nAltered = 0
        for stat in stats:
            sum_delay = sum_delay + stat["delay"]
            if stat["state"] == "CANCELED":
                nCancelled = nCancelled + 1
            elif stat["state"] == "MODIFIED":
                nAltered = nAltered + 1
        averageDelay = int(sum_delay / daysMonitoring)

        return_msg = f"🕛  Ritardo medio: <b>{averageDelay} min</b>"
        return_msg += f"\n❌  Corse cancellate: <b>{nCancelled}</b>"
        return_msg += f"\n❗  Corse alterate: <b>{nAltered}</b>"

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
        if isinstance(day_dict[day], tuple):
            return day_dict[day]

    bot_msg = f"📊 <b>STATISTICHE Treno {train_code}</b>\n\n"
    bot_msg += "<b>STATISTICHE ultimi 30 giorni</b>\n"
    bot_msg += day_dict[30]
    bot_msg += "\n\n<b>STATISTICHE ultimi 120 giorni</b>\n"
    bot_msg += day_dict[120]
    bot_msg += "\n\n⚠️ Questi dati possono non essere affidabili, sono solo a scopo indicativo.\nSe vuoi maggiori indicazioni premi 'Statistiche Dettagliate'"

    return (bot_msg, rankingButtons())
