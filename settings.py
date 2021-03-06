import json
import os

from datetime import datetime

OUTPUT_DIR = os.environ["OUTPUT_DIR"]
LOGS_DIR = os.environ["LOGS_DIR"]
JOBS_JSON_FILE = os.environ["JOBS_JSON_FILE"]

EXECUTION_TIMESTAMP = datetime.now().strftime("%m-%d-%Y-%H-%M-00")
MAIN_LOG_FILE = f"{LOGS_DIR}/{EXECUTION_TIMESTAMP}_main.log"

FROM_EMAIL = os.environ["FROM_EMAIL"]
ADMIN_EMAILS = json.loads(os.environ["ADMIN_EMAILS"])
CLIENT_EMAILS = json.loads(os.environ["CLIENT_EMAILS"])

ATTACHMENTS_DIR = "mailer/attachments"

SUCCESS_SUBJECT = os.environ["SUCCESS_SUBJECT"]
FAILURE_SUBJECT = os.environ["FAILURE_SUBJECT"]
SUCCESS_BODY = os.environ["SUCCESS_BODY"]
FAILURE_BODY = os.environ["FAILURE_BODY"]
