from flask import render_template
from .. import backend_api

def index():
    stats = backend_api.get_general_stats()
    return render_template("pages/index.html.j2", stats=stats)
