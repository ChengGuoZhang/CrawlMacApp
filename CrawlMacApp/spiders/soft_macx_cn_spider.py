# -*- coding: utf-8 -*-
import re
import scrapy
import sys
from scrapy.spiders import CrawlSpider, Spider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
import time
from CrawlMacApp.items import CrawlmacappItem


class MacxSpider(Spider):
    name = "soft_macx_cn"
    download_delay = 0
    allowed_domains = ["soft.macx.cn"]
    start_urls = ['http://soft.macx.cn/']
    base_url = 'http://soft.macx.cn/'

    def parse(self, response):
        reg = re.compile(r"第(.*?)页/共(.*?)页")
        #response_tmp = unicode(response.body, 'GB18030').encode('UTF-8')
        response_tmp = response.body.decode('GB18030').encode('UTF-8')
        total_page_num = re.findall(reg,response_tmp)[0][1]
        #print response_tmp.decode('UTF-8').encode('GBK')
        for page in range(1,int(total_page_num)+1):
            request=scrapy.Request("http://soft.macx.cn/index.asp?page="+str(page)+"&classid=&cpu=&keyword=&order=",callback=self.parse_per_page)
            yield request

    def parse_per_page(self,response):
        # if set the regex to r'/[0-9]{0,5}\.htm' ,it will match the software in left side of the website which don't have date filed
        reg = re.compile(r'href="/[0-9]{0,5}\.htm"')
        url_pure_num = re.findall(reg,response.body)
        soft_id = set()
        reg = re.compile(r'[0-9]{1,5}')

        for id in url_pure_num:
            id = id.replace('href=','')
            id = id.replace('"','')
            id_num = re.findall(reg,id)[0]
            # 6013 doesn't has the date filed,So ignore it.what's more ,soft6103 is the website official Application
            if (int(id_num)!=6103):
                date_selector = response.selector.xpath('//a[contains(@href,"' + id + '")]/parent::div/parent::li/span[contains(@class,"description")]/span[contains(@class,"date")]/text()').extract()
                if (len(date_selector) == 0 ):
                    # in the page 12, i find the error of the website itsekf, it put the date filed in the wrong position,so we munully adjust the date to defult 20161124
                    date = '20161124'
                elif (len(date_selector) == 1):
                    date = date_selector[0].strip('\n').strip('\t').replace('-','')
                elif (len(date_selector) == 2):
                    #the latest software have two element
                    date = time.strftime('%Y%m%d',time.localtime())
                    date = self.FormatTime(date)
            else:
                continue
            # use the last  num to decide the length of the real_soft_id
            soft_unique_id = id_num+date+str(len(id_num))
            soft_id.add(int(soft_unique_id))

        with open("soft_id\\soft_macx_cn_id.txt","a+") as fp:
            lines = fp.readlines()
            soft_id_txt = []
            for line in lines:
                soft_id_txt.append(int(line))
            for id in soft_id.copy():   # avoid the error: in the iteration we can't delete element
                if id in soft_id_txt:
                    soft_id.remove(id)
                    continue
                # extract the real soft id in such XXXX201601014
                real_soft_id = str(id)[0:int(str(id)[-1])]
                url = MacxSpider.base_url + real_soft_id + ".htm"
                request = scrapy.Request(url,callback=self.parse_per_soft,meta={"soft_id":int(real_soft_id)})
                yield  request
            for id in soft_id:
                fp.write(str(id)+'\n')

    def parse_per_soft(self,response):
        download_url = response.selector.xpath(
            '//a[contains(@rel,"facebox") and contains(@class,"button is-primary") and not(contains(@target,"_blank"))]/@href').extract()
        download_url = MacxSpider.base_url + download_url[0]
        soft_id = response.meta['soft_id']
        soft_name = response.selector.xpath('//div[contains(@class,"sname")]/h2/text()').extract()[0]
        soft_desc = response.selector.xpath('//div[contains(@id,"pdescr")]/h/span/text()').extract()[0]
        soft_info ={"soft_id":soft_id,"soft_name":soft_name,"soft_desc":soft_desc}
        request = scrapy.Request(download_url,callback=self.parse_per_download,meta=soft_info)
        yield request

    def parse_per_download(self,response):
        real_download_url = response.selector.xpath(
            '//a[contains(@rel,"facebox") and contains(@class,"button is-primary") and not(contains(@target,"_blank"))]/@href').extract()[0]
        # softwares in itunes can be downloaded directly
        if (real_download_url.find("itunes.apple.com")== -1):
            if real_download_url.find(r".dmg") != -1 or real_download_url.find(r".pkg") != -1:
                item = CrawlmacappItem()
                item['soft_id'] = response.meta['soft_id']
                item['soft_name'] = response.meta['soft_name']
                item['download_link'] = real_download_url
                item['is_download'] = False
                item['download_time'] =""
                item['soft_sha256'] =""
                item['is_upload_ftp'] = False
                item['upload_time'] =""
                item['upload_file_name'] = ""
                item['download_http_error'] = False
                item['soft_desc'] = response.meta['soft_desc']


                yield item

    def FormatTime(self,t):
        # delete the zero in 20170101 - > 201711 which can uniform with the date field in the website
        if (t[4] == '0'):
            t = t[0:4]+t[5:8]
        if (t[-2] == '0'):
            t = t[:-3]+t[-2:-1]
        return t
