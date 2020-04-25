import requests


class TrainNotFoundException(Exception):
    pass


# request the Station_ID of the train by the number of the train.
# For the requets both the Number and Station_ID are necessary for the query. Then i must have the Statation_ID from the number given by user
def find_station_id(train_number):
    try:
        response = requests.get(
            "http://www.viaggiatreno.it/viaggiatrenonew/resteasy/viaggiatreno/cercaNumeroTrenoTrenoAutocomplete/%s"
            % train_number
        )
    except requests.ConnectionError:
        raise ConnectionError  # probably the trenitalia API are offline
    response.encoding = "utf-8"
    response = response.text
    if len(response) != 0 and "<H1>" not in response and response is not None:
        if (
            "-" in response
        ):  # this thing is necessary because for some reasons there are train with the same number but different station_ID.
            response = response[(response.index("|") + 1) :]
            response = response[(response.index("-") + 1) : (response.index("\n"))]
            return response  # return the ID of the train
        else:
            raise TrainNotFoundException  # Il treno non esiste


def train_status(station_id, train_number):
    # See api docs: the request urls is composed by TRAIN_ID/TRAIN_NUMBER
    response = requests.get(
        f"http://www.viaggiatreno.it/viaggiatrenomobile/resteasy/viaggiatreno/andamentoTreno/{station_id}/{train_number}"
    )
    return response.json()
