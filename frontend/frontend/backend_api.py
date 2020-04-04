import os

import requests
import requests_mock

API_BASE_URL = "http://backend/api"

r = requests.session()
if os.environ.get("MOCK_API"):
    adapter = requests_mock.Adapter()
    adapter.register_uri(
        "GET", f"{API_BASE_URL}/stats/train/not_registered", status_code=404
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/stats/train/no_stats",
        status_code=200,
        json={"stats": []},
    )
    adapter.register_uri(
        "GET",
        f"{API_BASE_URL}/stats/train/with_stats",
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
        "POST",
        f"{API_BASE_URL}/stats/train",
        status_code=200,
        json={"message": "OK, train registered"},
    )
    r.mount(API_BASE_URL, adapter)


def get_train_stats(train_id: str):
    response = r.get(f"{API_BASE_URL}/stats/train/{train_id}")
    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise Exception("Something wrong with the backend")

    return response.json()


def register_train(train_id: str):
    response = r.post(f"{API_BASE_URL}/stats/train")
    if response.status_code == 404:
        return None

    if response.status_code != 200:
        raise Exception("Something wrong with the backend")

    return response.json()
