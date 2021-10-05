import os

from scrapy.crawler import CrawlerProcess
from scrapper.spiders.maxiconsumo import MaxiconsumoSpider
from scrapper.spiders.yaguar import YaguarSpider


if __name__ == "__main__":

    # os.environ.get('JOBS')
    # exit()

    process = CrawlerProcess({
        # 'DOWNLOAD_DELAY': 0.25,
        'DOWNLOAD_DELAY': 0,
        'FEED_URI': 'maxiconsumo_limpieza.csv',
        'FEED_FORMAT': 'csv'
    })
    # process.crawl(
    #     MaxiconsumoSpider,
    #     category="limpieza",
    #     max_pages=1
    # )
    process.crawl(
        YaguarSpider,
        category="limpieza",
        # max_pages=1
    )
    process.start()
