import requests

CLIENT_ID = 44922
CLIENT_SECRET = "6b1c35b41cd597efd12ab210411ff0a8c5a0c1c8"
ACCESS_TOKEN = "fd68349922f8c1eaa01595f5d8693d1d53b76352"
MAX_READ_REQUESTS_PER_15MIN = 100
MAX_READ_REQUESTS_PER_DAY = 1000
URL_BASE = "https://www.strava.com/api/v3"
ATHLETE_ID = 33468374
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


def get_activities() -> list:
    endpoint = f"athlete/activities"

    params = dict(
        before=None,
        after=None,
        page=1,
        per_page=30,
    )
    routes = get_endpoint(endpoint, params)
    return routes


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