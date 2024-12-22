import os
import json
import requests
import logging

logger = logging.getLogger(__name__)
CLIENT_ID = 44922
CLIENT_SECRET = "6b1c35b41cd597efd12ab210411ff0a8c5a0c1c8"
ACCESS_TOKEN = "4a86af9a6bfbc704349e50f7997abe242c314b09"
MAX_READ_REQUESTS_PER_15MIN = 100
MAX_READ_REQUESTS_PER_DAY = 1000
MAX_PER_PAGE = 200
URL_BASE = "https://www.strava.com/api/v3"
ATHLETE_ID = 33468374
REFRESH_TOKEN = "81c37f5e837468c0efd34f58f3a89934d8f5fb43"
AUTH_CODE = "e2ad12f5fdd15b9567d0bc61c30450d3b00684e6"


def get_endpoint(endpoint: str, params: dict) -> dict | list:
    url = f"{URL_BASE}/{endpoint}"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }
    res = requests.get(url=url, headers=headers, params=params)
    if res.ok:
        result = res.json()
        return result
    else:
        raise ValueError(f"status code: {res.status_code} {res.text}")


def get_athlete() -> dict:
    return get_endpoint("athlete", params=dict())


def get_activities(page: int = 1, per_page: int = MAX_PER_PAGE) -> list:
    endpoint = f"athlete/activities"
    params = dict(
        before=None,
        after=None,
        page=page,
        per_page=per_page,
    )
    routes = get_endpoint(endpoint, params)
    return routes


def log_activities(page: int, per_page: int) -> int:
    activities = get_activities(page, per_page)
    n_act = len(activities)
    with open(os.path.join("outputs", f"activities_{page:04d}.json"), "w") as fp:
        json.dump(activities, fp, indent=2)
        logging.info(f"logged {n_act=} activities in page {page:04d}")
        return n_act


def is_logged(page: int) -> bool:
    return os.path.isfile(os.path.join("outputs", f"activities_{page:04d}.json"))


def log_all_activities() -> None:
    """To fully go through the full set of results, iterate until an empty page is returned."""
    page = 0
    n_per_page = MAX_PER_PAGE
    stop = False
    while not stop:
        if not is_logged(page):
            n_act_logged = log_activities(page, n_per_page)
            stop = n_act_logged == 0
        page += 1


def post_token() -> dict:
    res = requests.post(
        url="https://www.strava.com/oauth/token",
        params=dict(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            code=AUTH_CODE,
            grant_type="authorization_code",
            scope="activity:read",
        )
    )
    if res.ok:
        result = res.json()
        return result
    else:
        raise ValueError(f"status code: {res.status_code} {res.text}")


def refresh_token() -> dict:
    res = requests.post(
        url="https://www.strava.com/oauth/token",
        params=dict(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            grant_type="refresh_token",
            refresh_token=REFRESH_TOKEN,
        )
    )
    if res.ok:
        result = res.json()
        return result
    else:
        raise ValueError(f"status code: {res.status_code} {res.text}")