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

    def already_exist(self,soft_uniq_id):
        soft_uniq_id = int(soft_uniq_id.replace('-',''))
        with open("soft_id\\rj_baidu_com_id.txt", "a+") as fp:
            lines = fp.readlines()
            soft_id_txt = []
            for line in lines:
                soft_id_txt.append(int(line))
            if soft_uniq_id in soft_id_txt:
                return True
            else:
                fp.write(str(soft_uniq_id)+'\n')
                return False



    def parse_per_page(self,response):
        soft_ids = response.selector.xpath('//div[contains(@class,"download")]/a/@sid').extract()
        download_urls = response.selector.xpath('//div[contains(@class,"download")]/a/@href').extract()
        soft_names = response.selector.xpath('//div[contains(@class,"softInfo")]/p[contains(@class,"title")]/a/text()').extract()
        soft_descs = response.selector.xpath('//div[contains(@class,"softInfo")]/p[contains(@class,"desc")]/text()').extract()
        soft_update_time = response.selector.xpath('//div[contains(@class,"softInfo")]/p[contains(@class,"info")]/font[2]/text()').extract()

        length = len(soft_ids)
        for i in range(0,length):
            if download_urls[i].find(r".dmg") != -1 or download_urls[i].find(r".pkg") != -1:
                soft_uniq_id = soft_ids[i] + soft_update_time[i]
                if self.already_exist(soft_uniq_id):
                    continue
                item = CrawlmacappItem()
                item['soft_id'] = int(soft_ids[i])
                item['soft_name'] = soft_names[i]
                item['download_link'] = download_urls[i]
                item['is_download'] = False
                item['download_time'] = ""
                item['soft_sha256'] = ""
                item['is_upload_ftp'] = False
                item['upload_time'] = ""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = soft_descs[i]
                yield item




