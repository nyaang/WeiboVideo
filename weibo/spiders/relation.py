# -*- coding: utf-8 -*-
import scrapy
import re
import json

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from weibo.items import WeiboUrl
from values import FILENAME_COOKIES, URL_REGEX, HREF_REGEX


class Relation(CrawlSpider):
    name = "relation"
    start_urls = ["http://weibo.com/tv/"]
    rules = [
        Rule(
            LinkExtractor(allow=URL_REGEX),
            callback='parse_url',
            follow=True
        ),
    ]
    cookies = {}

    def __init__(self, *a, **kw):
        super(Relation, self).__init__(*a, **kw)
        try:
            file = open(FILENAME_COOKIES,'r',encoding='utf-8')
            for cookie in json.load(file)["cookies"]:
                self.cookies[cookie["name"]]=cookie["value"]
        except:
            print('cannot load ', FILENAME_COOKIES)
            exit(1)

    def start_requests(self):
        for url in self.start_urls:
            req = scrapy.Request(url, cookies=self.cookies, dont_filter=True)
            yield req

    def parse_url(self, response):
        u = WeiboUrl()
        u["from_url"] = ''.join(re.findall(HREF_REGEX, response.request.headers["Referer"].decode()))
        u["url"] = ''.join(re.findall(HREF_REGEX, str(response)))
        yield u
