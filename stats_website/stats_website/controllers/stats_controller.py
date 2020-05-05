"""
This controller handles pages about the train(s) stats
"""

from flask import request, jsonify, render_template, redirect, url_for

from .. import backend_api


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

    backend_response = backend_api.get_train_stats(train_id)
    if backend_response:
        return render_template(
            "train/stats.html.j2",
            train_id=train_id,
            stats=backend_response.get("stats"),
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
