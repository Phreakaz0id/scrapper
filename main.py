from jobs.runner import run_jobs
from jobs.fetcher import fetch_jobs

from logzero import logger, logfile

from settings import MAIN_LOG_FILE

from twisted.internet import reactor


if __name__ == "__main__":
    # Initializing log file
    logfile(MAIN_LOG_FILE)
    logger.info("🏃‍♀️ [Main] Script starts and will: fetch jobs, run jobs.")
    # Fetches jobs
    jobs = fetch_jobs()
    # Runs jobs
    run_jobs(jobs)
    reactor.run()
