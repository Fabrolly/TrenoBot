"""
This controller handles pages about the train(s) stats
"""
import json

from flask import request, jsonify, render_template, redirect, url_for

from .. import backend_api
import requests


def view():
    """
    .. :quickref: Page; Get single train stats

    Show the stats related to a certain train.
    Handles the case of a missing train.
    Warn the user if the train was just inserted.
    """
    train_id = request.args.get("train")
    if train_id is None or train_id.strip() == "":
        return "Bad request", 400

    is_filtered = False
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    if from_date and to_date:
        is_filtered = True

    backend_response = backend_api.get_train_stats(train_id, from_date, to_date)
    stats = backend_response.get("stats")
    if request.args.getlist("only_status"):
        only_status = request.args.getlist("only_status")
        stats = list(filter(lambda s: s["state"] in only_status, stats))
        is_filtered = True
    if request.args.get("min_delay"):
        min_delay = int(request.args.get("min_delay"))
        stats = list(filter(lambda s: s["delay"] >= min_delay, stats))
        is_filtered = True

    train_information = backend_api.get_train_information(train_id)
    n_stations = len(train_information.get("fermate")) if train_information else 1

    if backend_response:
        return render_template(
            "train/stats.html.j2",
            train_id=train_id,
            stats=json.dumps(stats),
            stats_py=stats,
            is_filtered=is_filtered,
            n_stations=n_stations,
            form={
                "min_delay": request.args.get("min_delay"),
                "only_status": request.args.getlist("only_status"),
            },
            created=backend_response.get("created", False),
        )
    else:
        return render_template("train/stats.html.j2", train_id=train_id, stats=None,)


def ranking():
    """
    .. :quickref: Page; Get ranking of the trains

    Show the ranking of the trains.
    """
    ranking_response = backend_api.get_ranking()
    return render_template(
        "train/ranking.html.j2",
        best_trains=ranking_response["best"],
        worst_trains=ranking_response["worst"],
    )
