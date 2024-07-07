import logging
import os
import json
from strava_backup import api_client


logging.basicConfig(level="INFO")
athlete = api_client.get_athlete()
logging.info(athlete)
with open(os.path.join("outputs", "athlete.json"), "w") as fp:
    json.dump(athlete, fp, indent=2)
logging.info("completed")
