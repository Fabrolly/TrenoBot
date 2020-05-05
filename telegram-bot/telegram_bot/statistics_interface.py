"""
A module that use API to retrive various types of stats about train in backend
"""
import requests
import json
import os


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
