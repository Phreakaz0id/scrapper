import os

from datetime import datetime

from logzero import logger, logfile

from scrapper.spiders.maxiconsumo import MaxiconsumoSpider
from scrapper.spiders.yaguar import YaguarSpider

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from settings import EXECUTION_TIMESTAMP, LOGS_DIR, MAIN_LOG_FILE

from twisted.internet import reactor, defer


os.environ['SCRAPY_SETTINGS_MODULE'] = 'scrapper.settings'
scrapy_settings = get_project_settings()
scrapy_settings.set('ITEM_PIPELINES', {
    'scrapper.pipelines.MultiCSVItemPipeline': 300,
})

MODULE = __name__


def get_spider_by_type(_type):
    types = {
        "yaguar": YaguarSpider,
        "maxiconsumo": MaxiconsumoSpider
    }
    return types[_type]


def build_logfile_name(job_type, category):
    return f"{LOGS_DIR}/{EXECUTION_TIMESTAMP}_{job_type}_{category}.log"


@defer.inlineCallbacks
def run_jobs(jobs):
    logger.info(f"[{MODULE}] 🛠 Preparing jobs runner with settings [scrapy_settings: {scrapy_settings.__dict__}].")
    runner = CrawlerRunner(settings=scrapy_settings)
    for job in jobs:
        job_type = job["settings"]["type"]
        spider = get_spider_by_type(job_type)
        args = job["args"]
        category = args["category"]

        logfile_name = build_logfile_name(job_type, category)

        # Switches to main logfile
        logfile(MAIN_LOG_FILE)
        logger.info(f"[{MODULE}] 🛠 Starting a {job_type}:{category} crawler and new log file: ({logfile_name}).")
        # Initializing log file
        logfile(logfile_name, maxBytes=1e6, backupCount=3)

        yield runner.crawl(spider, **args)

    reactor.stop()

    logfile(MAIN_LOG_FILE)
    logger.info(f"[{MODULE}]" + " 🏁 Finished all crawling jobs.\n")
