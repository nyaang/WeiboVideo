# -*- coding: utf-8 -*-
import scrapy
import re
import time
import json

from lxml import etree
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from weibo.items import WeiboInfo
from web_driver import GetCookies
from values import FILENAME_COOKIES, URL_REGEX, FILENAME_LINKS, URL_COMMENTS, HREF_REGEX, USERCARD_REGEX, MID_REGEX


class WeiboSpider(CrawlSpider):
    name = "weibotv"
    start_urls = None
    rules = [Rule(LinkExtractor(allow=URL_REGEX),callback='parse_video',),
    ]
    cookies = {}

    def get_links(self):
        try:
            links = json.load(open(FILENAME_LINKS, 'r', encoding='utf-8'))["links"]
            self.start_urls = links
        except FileNotFoundError:
            print('Cannot find links.json')
            exit(1)

    def get_cookies(self):
        try:
            file = open(FILENAME_COOKIES, 'r', encoding='utf-8')
        except FileNotFoundError:
            GetCookies().run()
            file = open(FILENAME_COOKIES, 'r', encoding='utf-8')
        for cookie in json.load(file)["cookies"]:
            self.cookies[cookie["name"]]= cookie["value"]

    def __init__(self, *a, **kw):
        self.start_urls = []
        self.get_cookies()
        self.get_links()
        super(WeiboSpider, self).__init__(*a, **kw)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=self.cookies, callback=self.parse_video)

    def generate_rnd(self):
        return str(int(time.time() * 1000))

    def parse_video(self, response):
        content = ''.join(response.xpath('//div[@class="info_txt W_f14"]/text()').extract())
        author = ''.join(response.xpath('//span[@class="W_f14 L_autocut bot_name W_fl"]/text()').extract())
        mid = ''.join(re.findall(MID_REGEX, ''.join(
                response.xpath('//a[@class="WB_cardmore S_txt1 S_line1 clearfix"]/@action-data').extract())
        ))
        url = ''.join(re.findall(HREF_REGEX, response.url))
        info = WeiboInfo()
        info.item["author"] = author
        info.item["content"] = content
        info.item["id"] = mid
        info.item["url"] = url
        try:
            info.comments_num = int(''.join(
                    response.xpath('//span[@node-type="comment_btn_text"]/span/em[2]/text()').extract()
                )
            )
        except ValueError:
            info.comments_num = 0
        try:
            info.likes_num = int(''.join(response.xpath('//span[@node-type="like_status"]/em[2]/text()').extract()))
        except ValueError:
            info.likes_num = 0
        try:
            info.forwards_num = int(''.join(response.xpath('//span[@node-type="forward_btn_text"]/span/em[2]/text()').extract()))
        except ValueError:
            info.forwards_num = 0
        info.forwards_page = info.forwards_num//15
        info.forwards_remain = info.forwards_page
        info.item["comments_num"] = info.comments_num
        info.item["likes_num"] = info.likes_num
        info.item["forwards_num"] = info.forwards_num
        info.item["comments"] = []
        info.item["forwards"] = []
        info.item["likes"] = []
        if info.forwards_num > 0:
            req_forwards = scrapy.Request(
                url='http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=%s&__rnd=%s' % (
                    info.item["id"],
                    self.generate_rnd()
                ),
                callback = self.parse_forwards,
                cookies=self.cookies,
            )
            req_forwards.meta["Item"] = info
            yield req_forwards
        elif info.comments_num > 0:
            req_comments = scrapy.Request(
                url='http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&filter=all&from=singleWeiBo&__rnd=%s' % (
                    info.item["id"],
                    self.generate_rnd()
                ),
                callback=self.parse_comments,
                cookies=self.cookies
            )
            req_comments.meta["Item"] = info
            yield req_comments
        else:
            yield info.item

    def parse_comments(self, response):
        info = response.meta["Item"]
        process_comments_num = 0
        try:
            objs = etree.HTML(json.loads(response.body.decode())["data"]["html"])
            cmt = objs.xpath('//div[@class="list_li S_line1 clearfix"]')
            for c in cmt:
                comment_content = ''.join(c.xpath('.//div[@class="WB_text"]/text()')).split() if len(
                    c.xpath('.//div[@class="WB_text"]/a[2]/text()')) == 0 else ''.join(
                    ''.join(c.xpath('.//div[@class="WB_text"]/text()')).split())
                comment_usercard = ''.join(
                    re.findall(r'\d{10}', ''.join(c.xpath('.//div[@class="WB_text"]/a/@usercard'))))
                comment_id = ''.join(c.xpath('./@comment_id'))
                comment_likes = ''.join(c.xpath('.//span[@node-type="like_status"]/em[2]/text()'))
                try:
                    comment_likes = int(comment_likes)
                except Exception:
                    comment_likes = 0
                info.item["comments"].append({
                        "comment_content": comment_content,
                        "comment_usercard": comment_usercard,
                        "comment_id": comment_id,
                        "comment_likes": comment_likes
                    }
                )
                process_comments_num += 1
        except Exception:
            print("comment page failed to load!\n")
        if info.comments_num == 0:
            yield info.item
        else:
            if info.comments_num >= 15:
                info.comments_current_page += 1
                root_comment_max_id = str(int(info.item["comments"][info.comments_now - 1]["comment_id"]) - 1)
                info.comments_now += process_comments_num
                info.comments_num -= process_comments_num
            else:
                info.comments_current_page += 1
                root_comment_max_id = str(int(info.item["comments"][info.comments_now - 1]["comment_id"]) - 1)
                info.comments_num = 0
                info.comments_now = info.item["comments_num"]
            req = scrapy.Request(
                url= URL_COMMENTS % (
                    info.item["id"],
                    root_comment_max_id,
                    str(info.comments_current_page),
                    str(info.comments_now),
                    self.generate_rnd()
                ),
                callback=self.parse_comments,
                cookies=self.cookies,
            )
            req.meta["Item"] = info
            yield req

    def parse_forwards(self, response):
        info = response.meta["Item"]
        try:
            objs = etree.HTML(json.loads(response.body.decode())["data"]["html"])
            fwd = objs.xpath('//div[@class="list_li S_line1 clearfix"]')
            begin = 0
            if info.max_id is None:
                if len(fwd) > 20:
                    begin = len(fwd) - 20
                info.max_id = ''.join(fwd[begin].xpath('//div[1]/@mid'))
            else:
                for f in fwd[begin:]:
                    forward_usercard = ''.join(
                        re.findall(USERCARD_REGEX, ''.join(f.xpath('.//div[@class="WB_text"]/a/@usercard'))))
                    info.item["forwards"].append({
                        "forward_usercard": forward_usercard,
                        }
                    )
        except:
            print("forward page failed to load!\n")
        if info.forwards_remain == 0:
            if info.comments_num > 0:
                req_comments = scrapy.Request(
                    url='http://weibo.com/aj/v6/comment/big?ajwvr=6&id=%s&filter=all&from=singleWeiBo&__rnd=%s' % (
                    info.item["id"],
                    self.generate_rnd()
                    ),
                    callback=self.parse_comments,
                    cookies=self.cookies
                )
                req_comments.meta["Item"] = info
                yield req_comments
            else:
                yield info.item
        else:
            info.forwards_current_page += 1
            info.forwards_remain -= 1
            req = scrapy.Request(
                url='http://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=%s&max_id=%s&page=%s&__rnd=%s' % (
                    info.item["id"],
                    info.max_id,
                    str(info.forwards_current_page),
                    self.generate_rnd()
                ),
                callback=self.parse_forwards,
                cookies=self.cookies,
            )
            req.meta["Item"] = info
            yield req
