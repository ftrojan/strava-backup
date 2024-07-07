import logging
import os
import json
from strava_backup import api_client


logging.basicConfig(level="INFO")
activities = api_client.get_activities()
logging.info(f"{len(activities)} activities")
with open(os.path.join("outputs", "activities.json"), "w") as fp:
    json.dump(activities, fp, indent=2)
logging.info("completed")
