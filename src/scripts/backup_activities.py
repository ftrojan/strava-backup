import logging
from strava_backup import api_client


logging.basicConfig(level="INFO")
logging.info("started")
api_client.log_all_activities()
logging.info("completed")
