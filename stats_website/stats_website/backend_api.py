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
                {"day": 1, "delay": -1},
                {"day": 2, "delay": 1},
                {"day": 3, "delay": 4},
                {"day": 4, "delay": 3},
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


def get_train_stats(train_id: str) -> typing.Dict:
    """
    Get the stats of a certain train from the backend

    Args:
        train_id: id of the train to get the data

    Returns:
        The train status
    """
    response = r.get(f"{API_BASE_URL}/train/{train_id}/stats")
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
