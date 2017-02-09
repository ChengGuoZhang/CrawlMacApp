# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

from CrawlMacApp.items import CrawlmacappItem


class BaiduCrawlSpider(scrapy.Spider):
    name = "rj_baidu_com"
    allowed_domains = ["rj.baidu.com"]
    start_urls = ['http://rj.baidu.com/search/index/?kw=mac']
    base_url = start_urls[0]
    #to avoid been banned
    download_delay = 2


    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url,self.parse,args={'wait':0.5})


    def parse(self, response):
        #print "_____________________________________________________________________"
        #page = response.body
        #page = page.decode('utf-8').encode('GB18030')
        #print "******************************************************************"
        page_num = response.selector.xpath('//div[contains(@class,"page")]/span[contains(@class,"pageList")]/a[6]/text()').extract()[0]
        for cur_page in range(1,int(page_num)+1):
            compose_url = BaiduCrawlSpider.base_url+"&pageNum="+str(cur_page)
            yield SplashRequest(compose_url,self.parse_per_page,args={'wait':0.5})


    def parse_per_page(self,response):
        print "_____________________________________________________________________"
        download_urls =response.selector.xpath('//div[contains(@class,"download")]/a/@href').extract()
        for url in download_urls:
            item = CrawlmacappItem()
            item['soft_id'] = "111"
            item['soft_name'] = "222"
            item['download_link'] = url
            item['is_download'] = False
            item['download_time'] = ""
            item['soft_sha256'] = ""
            item['is_upload_ftp'] = False
            item['upload_time'] = ""
            item['upload_file_name'] = ""
            item['download_http_error'] = False
            item['soft_desc'] = "333"
            yield item
        print "******************************************************************"



