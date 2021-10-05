# import os

from datetime import datetime
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapper.spiders.maxiconsumo import MaxiconsumoSpider
from scrapper.spiders.yaguar import YaguarSpider


def get_spider_by_type(_type):
    types = {
        "yaguar": YaguarSpider,
        "maxiconsumo": MaxiconsumoSpider
    }
    return types[_type]


if __name__ == "__main__":

    # os.environ.get('JOBS')
    # exit()

    jobs = [
        {
            "settings": {
                "feed_format": "csv",
                "type": "maxiconsumo"
            },
            "args": {
                "category": "limpieza",
                "max_pages": 1,
                "custom_settings": {
                    'FEED_URI': 'now_maxiconsumo_limpieza.csv'
                }
                # "max_pages": 14
            }
        },
        # {
        #     "settings": {
        #         "feed_format": "csv",
        #         "type": "maxiconsumo"
        #     },
        #     "args": {
        #         "category": "perfumeria",
        #         "max_pages": 1
        #         # "max_pages": 18
        #     }
        # }
    ]

    now = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

    for job in jobs:
        feed_format = job["settings"]["feed_format"]
        job_type = job["settings"]["type"]
        category = job["args"]["category"]

        args = job["args"]

        process = CrawlerProcess({
            # 'DOWNLOAD_DELAY': 0.25,
            'DOWNLOAD_DELAY': 0,
            # 'FEED_URI': f"{now}_{job_type}_{category}.csv",
            # 'FEED_URI': f"{now}_{job_type}_{category}.csv",
            'FEED_FORMAT': feed_format
        })
        spider = get_spider_by_type(job_type)
        process.crawl(
            spider,
            **args
        )
        # d = runner.join()
        # d.addBoth(lambda _: reactor.stop())
        process.start()
