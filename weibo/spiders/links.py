# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json

from lxml import etree
from web_driver import GetCookies
from values import FILENAME_LINKS, FILENAME_COOKIES
from values import URL_FIRST_PAGE, URL_OTHER_PAGE
from values import HREF_REGEX


class LinkSpider(scrapy.Spider):
    name = "links"
    start_urls = []
    urls = None
    cookies = {}

    def get_cookies(self):
        try:
            file = open(FILENAME_COOKIES, 'r', encoding='utf-8')
        except FileNotFoundError:
            GetCookies().run()
            file = open(FILENAME_COOKIES, 'r', encoding='utf-8')
        for cookie in json.load(file)["cookies"]:
            self.cookies[cookie["name"]]= cookie["value"]
        file.close()

    def get_links(self, page_want, each_page):
        current_page = 1
        pre_page = 1
        page = 1
        self.urls = {"links": set()}
        for i in range(page_want):
            page_bar = 0
            for j in range(each_page):
                self.start_urls.append(URL_FIRST_PAGE % (
                    str(page_bar), str(current_page), str(pre_page), str(page), self.generate_rnd)
                                       )
                page_bar += 1
                current_page += 1
            page += 1
            self.start_urls.append(URL_OTHER_PAGE % (
                str(pre_page), str(page), str(current_page), self.generate_rnd)
                                   )
            pre_page += 1

    def __init__(self, page_want=2, each_page=5):
        self.start_urls = []
        self.get_cookies()
        self.get_links(page_want, each_page)
        super(LinkSpider, self).__init__(name=self.name, start_urls=self.start_urls)

    def close(self, reason):
        file = open(FILENAME_LINKS, 'w', encoding='utf-8')
        self.urls["links"] = list(self.urls["links"])
        json.dump(self.urls, file, indent=4, sort_keys=False, ensure_ascii=False)
        file.close()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies)

    def parse(self, response):
        objs = etree.HTML(json.loads(response.body.decode())["data"])
        for d in objs.xpath('//div[@class="WB_detail"]'):
            href = ''.join(d.xpath('.//a[@node-type="feed_list_item_date"]/@href'))
            href = ''.join(re.findall(HREF_REGEX, href)[-1])
            self.urls["links"].add("http://weibo.com/tv/v/" + href)

    def generate_rnd(self):
        return str(int(time.time() * 1000))
