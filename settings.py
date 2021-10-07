import os

from datetime import datetime

OUTPUT_DIR = os.environ["OUTPUT_DIR"]
LOGS_DIR = os.environ["LOGS_DIR"]
JOBS_JSON_FILE = os.environ["JOBS_JSON_FILE"]

EXECUTION_TIMESTAMP = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
MAIN_LOG_FILE = f"{LOGS_DIR}/{EXECUTION_TIMESTAMP}_main.log"
