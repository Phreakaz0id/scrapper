# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from settings import OUTPUT_DIR
from datetime import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import CsvItemExporter
from scrapper import items

from settings import EXECUTION_TIMESTAMP


def build_file_name(spider_name, spider_category, file_extension):
    output_dir = OUTPUT_DIR + "/"
    full_path = output_dir + EXECUTION_TIMESTAMP + "_" + spider_name + "_" + spider_category + file_extension
    return full_path


class ScrapperPipeline:
    def process_item(self, item, spider):
        return item


def item_type(item):
    return type(item).__name__


class MultiCSVItemPipeline(object):
    defined_items = [name for name, _ in items.__dict__.items() if "Item" in name and name != "Item"]

    def open_spider(self, spider):
        self.files = dict(
            [
                (name, open(build_file_name(spider.name, spider.category, ".csv"), "w+b"))
                for name in self.defined_items
            ]
        )
        self.exporters = dict(
            [(name, CsvItemExporter(self.files[name])) for name in self.defined_items]
        )
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        item_name = item_type(item)
        if item_name in set(self.defined_items):
            self.exporters[item_name].export_item(item)
        return item
