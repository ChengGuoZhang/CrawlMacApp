# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy import signals
from scrapy.exporters import JsonItemExporter


class CrawlmacappPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = open('soft_macx_cn_items.json','a+b')
        tmp = ['soft_id', 'soft_name', 'download_link', 'is_download', 'download_time', 'soft_sha256',
               'upload_file_name', 'is_upload_ftp', 'upload_time','download_http_error', 'soft_desc', ]
        self.exporter = JsonItemExporter(self.file, ensure_ascii=False, fields_to_export=tmp)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        if (os.path.getsize('soft_macx_cn_items.json') == 0):
            self.exporter.start_exporting()
        else:
            self.file.seek(-1, os.SEEK_END)
            self.file.truncate()
            self.file.write(',')
            self.file.flush()

    def spider_closed(self, spider):
        self.file = open('soft_macx_cn_items.json', 'a+b')
        self.file.seek(-1, os.SEEK_END)
        if (self.file.read(1) == '}'):
            self.exporter.finish_exporting()
        else:
            self.file.seek(-1, os.SEEK_END)
            self.file.truncate()
            self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        self.file.flush()
        return item
