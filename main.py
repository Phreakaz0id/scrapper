import shutil
import os

from jobs.runner import run_jobs
from jobs.fetcher import fetch_jobs

from logzero import logger, logfile

from mailer.send_mail import notify_clients, notify_errors

from settings import EXECUTION_TIMESTAMP, MAIN_LOG_FILE, OUTPUT_DIR, LOGS_DIR, ATTACHMENTS_DIR

from twisted.internet import reactor

MODULE = __name__


def copy_files(source_dir, destination_dir):
    logfile(MAIN_LOG_FILE)
    source_path = os.path.dirname(__file__) + source_dir
    destination_path = os.path.dirname(__file__) + destination_dir

    logger.info(f"{MODULE} 📁 Preparing files to copy from: '{source_path}' into '{destination_path}'.")
    files = list(
        filter(
            lambda f: EXECUTION_TIMESTAMP in f,
            os.listdir(source_path)))

    if files == []:
        logger.info(f"{MODULE} 📁 No files to copy as attachments, skipping.")
        return

    logger.info(f"{MODULE} 📁 The following files will be copied {', '.join(files)}.")

    for file_name in files:
        full_file_name = os.path.join(source_path, file_name)
        if os.path.isfile(full_file_name):
            logger.info(f"{MODULE} 📁 Copying {full_file_name}...")
            shutil.copy(full_file_name, destination_path)
        full_destination_file_name = f"{destination_path}/{file_name}"

        # Check the files has been succesfulyl copied
        if os.path.isfile(full_destination_file_name):
            logger.info(f"{MODULE} 📁 Succesfully copied '{full_destination_file_name}'.")
        else:
            raise Exception(f"{MODULE} ❌ An unexpected error occurred while copying file: '{full_destination_file_name}'.")


def send_errors_report(error):
    try:
        logfile(MAIN_LOG_FILE)
        logger.error(error, exc_info=True)
        copy_files(LOGS_DIR, ATTACHMENTS_DIR)
        notify_errors()
    except Exception as e:
        logfile(MAIN_LOG_FILE)
        logger.error(f"{MODULE} ❌ An unexpected error occurred while sending error reports via email. Error:\n{e}.")


def main():
    try:
        # Initializing log file
        logfile(MAIN_LOG_FILE)
        logger.info(f"[{MODULE}] 🏃‍♀️ Script starts and will:\n* fetch jobs\n* run jobs\n* copy files into attachments\n* send output via email\n")
        # Fetches jobs
        jobs = fetch_jobs()
        # Prepare on finish callbacks
        on_finish_callbacks = [
            lambda: copy_files(OUTPUT_DIR, ATTACHMENTS_DIR),
            notify_clients
        ]
        # Runs jobs
        run_jobs(jobs, on_finish_callbacks=on_finish_callbacks)
        reactor.run()
    except Exception as e:
        send_errors_report(e)


if __name__ == "__main__":
    main()
