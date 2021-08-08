# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class ScrapperItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MaxiconsumoItem(Item):
    product_name = Field()
    code = Field()
    product_url = Field()
    bundle_price = Field()
    unit_price = Field()
