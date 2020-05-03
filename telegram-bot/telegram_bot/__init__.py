"""
This service offers a Telegram Bot that answers to user queries. The bot communicates with the ``backend`` service and uses a database instance to store informations about users and trains.

The service also runs a periodic job (trenordAlertChecker.py) that will update users in real time when something happens to their trains.

The following additional libraries are used:

* ``requests``: to handle interaction with the backend service
* ``telepot``: to handler interaction with the Telegram messaging platform
"""
