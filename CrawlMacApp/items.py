# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item

class CrawlmacappItem(Item):
    soft_id = scrapy.Field()
    soft_name = scrapy.Field()
    download_link = scrapy.Field()
    is_download = scrapy.Field()
    download_time = scrapy.Field()
    soft_sha256 = scrapy.Field()
    is_upload_ftp = scrapy.Field()
    upload_time = scrapy.Field()
    upload_file_name = scrapy.Field()
    download_http_error = scrapy.Field()
    soft_desc = scrapy.Field()
