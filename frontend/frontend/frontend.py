import time
from flask import Flask

from .controllers import page_controller, stats_controller

app = Flask(__name__)
app.add_url_rule("/", "index", page_controller.index, methods=["GET"])

app.add_url_rule("/stats/view", "stats.view", stats_controller.view, methods=["GET"])
app.add_url_rule(
    "/stats/register", "stats.register", stats_controller.register, methods=["POST"]
)
app.add_url_rule("/stats/ranking", "stats.ranking", stats_controller.ranking, methods=["GET"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
