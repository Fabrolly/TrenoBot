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
        "GET", f"{API_BASE_URL}/train/just_created", status_code=404, json={},
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/no_stats/stats",
        status_code=200,
        json={"stats": []},
    )
    adapter.register_uri(
        "GET", f"{API_BASE_URL}/train/no_stats", status_code=404, json={},
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats/stats",
        status_code=200,
        json={
            "stats": [
                {"date": "2020-05-10", "delay": -1, "state": "ON_TIME", "duration": 30},
                {"date": "2020-05-11", "delay": 1, "state": "DELAYED", "duration": 30},
                {"date": "2020-05-12", "delay": 4, "state": "DELAYED", "duration": 30},
                {
                    "date": "2020-05-13",
                    "delay": 30,
                    "state": "CANCELED",
                    "duration": 30,
                },
                {"date": "2020-05-14", "delay": 3, "state": "MODIFIED", "duration": 30},
                {"date": "2020-05-15", "delay": 3, "state": "DELAYED", "duration": 30},
                {"date": "2020-05-16", "delay": 3, "state": "DELAYED", "duration": 30},
            ],
        },
    ),
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats_2/stats",
        status_code=200,
        json={
            "stats": [
                {"date": "2020-05-10", "delay": -1, "state": "ON_TIME", "duration": 30},
                {"date": "2020-05-11", "delay": 1, "state": "DELAYED", "duration": 30},
                {
                    "date": "2020-05-13",
                    "delay": 30,
                    "state": "CANCELED",
                    "duration": 30,
                },
                {"date": "2020-05-15", "delay": 3, "state": "DELAYED", "duration": 30},
            ],
        },
    ),
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats/stats?from=2020-05-11&to=2020-05-14",
        status_code=200,
        json={
            "stats": [
                {"date": "2020-05-11", "delay": 1, "state": "DELAYED", "duration": 30},
                {"date": "2020-05-12", "delay": 4, "state": "DELAYED", "duration": 30},
                {
                    "date": "2020-05-13",
                    "delay": 30,
                    "state": "CANCELED",
                    "duration": 30,
                },
                {"date": "2020-05-14", "delay": 3, "state": "MODIFIED", "duration": 30},
            ],
        },
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats",
        status_code=200,
        json={
            "fermate": [
                {"id": "S01420", "progressivo": 1, "stazione": "COLICO"},
                {"id": "S01406", "progressivo": 2, "stazione": "PIONA"},
                {"id": "S01407", "progressivo": 3, "stazione": "DORIO"},
            ]
        },
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/train/with_stats_2",
        status_code=200,
        json={
            "fermate": [
                {"id": "S01420", "progressivo": 1, "stazione": "COLICO"},
                {"id": "S01407", "progressivo": 3, "stazione": "DORIO"},
            ]
        },
    )

    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/stats/ranking",
        status_code=200,
        json={
            "best": [
                {"id": 1, "delay": -2, "reliabilityIndex": 5},
                {"id": 3, "delay": -6, "reliabilityIndex": 4},
                {"id": 2, "delay": 0, "reliabilityIndex": 0},
            ],
            "worst": [
                {"id": 6, "delay": 30, "reliabilityIndex": -16},
                {"id": 5, "delay": 75, "reliabilityIndex": -62.5},
                {"id": 4, "delay": 45, "reliabilityIndex": -75},
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


def get_train_information(train_id: str) -> typing.Dict:
    """
    Get the information of a certain train from the backend

    Args:
        train_id: id of the train to get the data

    Returns:
        The train information
    """
    response = r.get(f"{API_BASE_URL}/train/{train_id}")
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
