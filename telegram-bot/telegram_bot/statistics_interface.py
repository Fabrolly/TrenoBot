import requests
import json

def train_ranking_readable():
    ranking = requests.get("http://backend:5000/api/stats/ranking").json()

    ranking_best = ranking['best'][:4]
    ranking_worst = ranking['worst'][:4]

    msg = "<i>Treno -> ritardo medio</i>\n\n"
    msg += "<b>Treni Migliori:\n</b>"

    for i in range (0, 4):
        msg += f'{str(i+1)}) '
        msg += str(ranking_best[i]['trainID'])
        msg += ' -> '
        msg += ranking_best[i]['delay'].split(".")[0]
        msg += ' min\n'

    msg += "<b>\nTreni Peggiori:\n</b>"

    for i in range (0, 4):
        msg += f'{str(i+1)}) '
        msg += str(ranking_worst[i]['trainID'])
        msg += ' -> '
        msg += ranking_worst[i]['delay'].split(".")[0]
        msg += ' min\n'


    return msg

