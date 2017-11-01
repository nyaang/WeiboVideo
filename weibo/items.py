# -*- coding: utf-8 -*-

import scrapy


class WeiboItem(scrapy.Item):
    author = scrapy.Field()
    content = scrapy.Field()
    id = scrapy.Field()
    url = scrapy.Field()
    comments = scrapy.Field()
    likes = scrapy.Field()
    forwards = scrapy.Field()
    comments_num = scrapy.Field()
    likes_num = scrapy.Field()
    forwards_num = scrapy.Field()


class WeiboUrl(scrapy.Item):
    from_url = scrapy.Field()
    url = scrapy.Field()


class WeiboInfo:
    item = None
    comments_num = None
    comments_now = None
    comments_current_page = None
    likes_num = None
    forwards_num = None
    forwards_page = None
    forwards_remain = None
    forwards_current_page = None
    max_id = None

    def __init__(self):
        self.item = WeiboItem()
        self.comments_num = 0
        self.comments_now = 0
        self.comments_current_page = 1
        self.likes_num = 0
        self.likes_page = 0
        self.likes_remain = 0
        self.likes_current_page = 1
        self.forwards_num = 0
        self.forwards_page = 0
        self.forwards_remain = 0
        self.forwards_current_page = 1
