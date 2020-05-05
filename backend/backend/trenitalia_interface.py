"""
A module to interface with the Trenitalia HTTP API
"""
import requests


class TrainNotFoundException(Exception):
    """
    An exception to represent the case in which a train is not found
    """

    pass


def find_station_id(train_number: int):
    """
    Find the station ID given a certain train number

    Args:
        train_number: train identifier

    Returns:
        the identifier of a station
    """
    try:
        response = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s"
            % train_number
        )
    except requests.ConnectionError:
        raise ConnectionError  # probably the trenitalia API are offline
    response.encoding = "utf-8"
    response_text = response.text
    if (
        len(response_text) != 0
        and "<H1>" not in response_text
        and response_text is not None
    ):
        if (
            "-" in response_text
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response_text = response_text[(response_text.index("|") + 1) :]
            response_text = response_text[
                (response_text.index("-") + 1) : (response_text.index("\n"))
            ]
            return response_text  # return the ID of the train
        else:
            raise TrainNotFoundException  # Il treno non esiste


def train_status(station_id, train_number):
    """
    Find the status of a train at a certain station

    Args:
        train_number: train identifier
        station_id: station identifier

    Returns:
        the status of the train
    """
    response = requests.get(
        f"http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/{station_id}/{train_number}"
    )
    return response.json()
