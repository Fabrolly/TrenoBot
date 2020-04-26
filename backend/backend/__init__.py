"""
The backend service is a flask-based REST API that allows
the services using it to retrieve real time and historical stats about trains.

On startup the backend service creates (if needed) a database to store all the required informations.

The backend service also runs a periodic job (check_journey.py) that will allow it to collect and keep track of historical stats.

Files and folders:

* ``tests/``: unit tests
* ``tests_integration/``: integration tests
* ``backend.py``: the entrypoint/main of the project, starting a flask instance
* ``check_journey.py``: a module offering utilities for the backrgound periodic checks
* ``database_initialization.yt``: a module exposing functions that will allow to work with a database
* ``database_utils.py``: a module exposing various functions to interact with the database
* ``trenitalia_interface.py``: a module to interact with the TrenItalia HTTP API
"""
