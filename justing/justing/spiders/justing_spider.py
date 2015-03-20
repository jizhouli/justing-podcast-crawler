#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
静雅思听
http://justing.com.cn/
'''

import os
import sys
import time
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request
from scrapy import log

from justing.items import JustingItem

class JustingSpider(CrawlSpider):
    name = 'justing'
    allowed_domains = ['justing.com.cn']

    def start_requests(self):
        '''
        '''
        requests = []
        log.start('./justing.log')

        req = Request(
                url = "http://justing.com.cn/"
                )
        req.meta['source'] = 'search|name'
        requests.append(req)

        return requests

    def parse(self, response):
        log.msg('-----\n%s\n-----' % str(response))
        item = JustingItem()
        item['title'] = 'hello'
        item['url'] = 'http://www.example.com'
        item['mp3_url'] = 'http://www.example.com/example.mp3'
        item['download'] = True
        log.msg(str(item))
        return item

