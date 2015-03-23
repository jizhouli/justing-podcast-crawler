#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
静雅思听
http://justing.com.cn/
'''

import os
import sys
import time

# FOR HTML DOM PARSE
#from scrapy.selector import HtmlXPathSelector # is deprecated
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

import urllib

from scrapy.contrib.spiders import CrawlSpider
from scrapy.http import Request, FormRequest
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

        # USAGE EXAMPLE COMMENT
        # req = Request(
        #         url = "http://justing.com.cn",
        #         )
        # req.meta['source'] = 'search|name'

        # 查询搜索结果
        req = FormRequest(
                url = "http://justing.com.cn/search_action.jsp",
                formdata = {
                    'searchType': 'name',
                    'searchWord': 'hello',
                    },

                headers = {
                    'Referer': 'http://justing.com.cn/',
                    },
                )
        req.meta['url_base'] = 'http://justing.com.cn'
        req.meta['mp3_base'] = 'http://dl.justing.com.cn/page/'
        requests.append(req)

        return requests

    # 解析搜索结果页
    def parse(self, response):
        #log.msg('-----\n%s\n-----' % str(response.body), level=log.DEBUG)
        log.msg('parse search result page: %s' % str(response))

        result = []

        # 创建选择器
        selector = Selector(response=response)
        # 获取结果页所有的Title节点列表
        title_nodes = selector.xpath("//div[@class='result']/h1")
        for title_node in title_nodes:
            href = title_node.xpath("./a/@href").extract()[0]
            title = title_node.xpath("./a/text()").extract()[0]

            title = title.replace(' ', '')
            #log.msg(title)

            url = response.meta['url_base'] + href
            #log.msg(url)

            log.msg(str(type(title)))
            urlencode_title = title # urllib.quote(title)
            mp3_url = response.meta['mp3_base'] + urlencode_title + '.mp3'
            #log.msg(mp3_url)

            item = JustingItem()
            item['title'] = title
            item['url'] = url
            item['mp3_url'] = mp3_url
            result.append(item)

        return result

