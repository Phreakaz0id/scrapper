import json

from logzero import logger
from settings import JOBS_JSON_FILE

MODULE = __name__


def fetch_jobs():
    logger.info(f"[{MODULE}]" + "🛠 Fetching jobs from json file using setting [JOBS_JSON_FILE={JOBS_JSON_FILE}].")
    f = open(JOBS_JSON_FILE)
    data = json.load(f)
    logger.info(f"[{MODULE}]" + "✅ Json file loaded succesfully.")
    f.close()
    return data
