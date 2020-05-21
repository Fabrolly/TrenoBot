"""
The stats website entrypoint, defining routes for the various pages of the webapp.
"""
import time
from flask import Flask

from .controllers import page_controller, stats_controller

app = Flask(__name__)
app.add_url_rule("/", "index", page_controller.index, methods=["GET"])

app.add_url_rule("/stats/view", "stats.view", stats_controller.view, methods=["GET"])
app.add_url_rule(
    "/stats/ranking", "stats.ranking", stats_controller.ranking, methods=["GET"]
)
app.add_url_rule(
    "/stats/compare", "stats.compare", stats_controller.compare, methods=["GET"]
)


def main(host: str = "0.0.0.0", port: int = 5000):
    """
    Runs the server on a certain host and port.
    The default hosts accepts all incoming connections.

    Args:
        host: address to listen on
        port: port to listen on
    """
    app.run(debug=True, host=host, port=port)


if __name__ == "__main__":
    main()
