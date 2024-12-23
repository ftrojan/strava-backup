import logging
import os
import json
from strava_backup import api_client


logging.basicConfig(level="INFO")
token = api_client.refresh_token()
logging.info(token)
with open(os.path.join("secrets", "fresh_token.json"), "w") as fp:
    json.dump(token, fp, indent=2)
logging.info("completed")
