"""
A module to interact with the HTTP API provided by the backend.

The module mocks methods if the environment variable "MOCK_API" is set.
"""
import os
import typing

import requests
import requests_mock

API_BASE_URL = "http://backend:5000/api"

r = requests.session()
if os.environ.get("MOCK_API"):
    adapter = requests_mock.Adapter()
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/just_created/stats",
        status_code=200,
        json={"created": True, "stats": []},
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/no_stats/stats",
        status_code=200,
        json={"stats": []},
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats/stats",
        status_code=200,
        json={
            "stats": [
                {"date": "2020-05-10", "delay": -1, "state": "ON_TIME"},
                {"date": "2020-05-11", "delay": 1, "state": "DELAYED"},
                {"date": "2020-05-12", "delay": 4, "state": "DELAYED"},
                {"date": "2020-05-13", "delay": 30, "state": "CANCELED"},
                {"date": "2020-05-14", "delay": 3, "state": "MODIFIED"},
                {"date": "2020-05-15", "delay": 3, "state": "DELAYED"},
            ],
        },
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats/stats?from=2020-05-11&to=2020-05-14",
        status_code=200,
        json={
            "stats": [
                {"date": "2020-05-11", "delay": 1, "state": "DELAYED"},
                {"date": "2020-05-12", "delay": 4, "state": "DELAYED"},
                {"date": "2020-05-13", "delay": 30, "state": "CANCELED"},
                {"date": "2020-05-14", "delay": 3, "state": "MODIFIED"},
            ],
        },
    )

    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/stats/ranking",
        status_code=200,
        json={
            "best": [
                {"id": 1, "delay": 0},
                {"id": 2, "delay": 1},
                {"id": 3, "delay": 3},
            ],
            "worst": [
                {"id": 6, "delay": 120},
                {"id": 5, "delay": 67},
                {"id": 4, "delay": 34},
            ],
        },
    )
    r.mount(API_BASE_URL, adapter)

    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/stats/general",
        status_code=200,
        json={"avg_delay": 42,},
    )
    r.mount(API_BASE_URL, adapter)


def get_train_stats(
    train_id: str, from_date: typing.Optional[str], to_date: typing.Optional[str]
) -> typing.Optional[typing.Dict]:
    """
    Get the stats of a certain train from the backend

    Args:
        train_id: id of the train to get the data
        from_date: ISO format date to select the starting point
        to_date: ISO format date to select the ending point

    Returns:
        The train status
    """
    params = {}
    if from_date and to_date:
        params["from"] = from_date
        params["to"] = to_date

    response = r.get(f"{API_BASE_URL}/train/{train_id}/stats", params=params)
    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise Exception("Something wrong with the backend")

    return response.json()


def get_ranking() -> typing.Dict:
    """
    Get the trains ranking from the backend

    Returns:
        The trains ranking
    """
    response = r.get(f"{API_BASE_URL}/stats/ranking")
    if response.status_code != 200:
        raise Exception("Something wrong with the backend")

    return response.json()


def get_general_stats() -> typing.Dict:
    """
    Get the general stats from the backend

    Returns:
        The general stats for the trains
    """
    response = r.get(f"{API_BASE_URL}/stats/general")
    if response.status_code != 200:
        raise Exception("Something wrong with the backend")

    return response.json()
