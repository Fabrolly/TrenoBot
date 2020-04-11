from flask import render_template
from .. import backend_api


def index():
    stats_response = backend_api.get_general_stats()
    return render_template("pages/index.html.j2", stats=stats_response["stats"])
