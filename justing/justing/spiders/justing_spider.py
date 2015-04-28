#!/usr/bin/env python
# -*- coding: utf8 -*-

'''
静雅思听
http://justing.com.cn/
'''

# FOR HTML DOM PARSE
#from scrapy.selector import HtmlXPathSelector # is deprecated
from scrapy.selector import Selector
#from scrapy.http import HtmlResponse

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

        # input parameters by command line -a

        # 判断 -a search_words 参数是否输入
        if not hasattr(self, 'search_words'):
            log.msg('search_words parameter is not input, please input like:\nscrapy crawl justing -a search_words="book1,book2"', level=log.ERROR)
            return requests

        # 判断 search_words 参数是否为空字符串
        if len(self.search_words) == 0: # pylint:disable=access-member-before-definition
            log.msg('search_words parameter is empty, please input like:\nscrapy crawl justing -a search_words="book1,book2"', level=log.ERROR)
            return requests

        self.search_words = self.search_words.split(',')
        log.msg(str(self.search_words))
        for word in self.search_words:
            req = FormRequest(
                    url = "http://justing.com.cn/search_action.jsp",
                    formdata = {
                        'searchType': 'name',
                        'searchWord': word,
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

            url = response.request.meta['url_base'] + href
            #log.msg(url)

            #log.msg(str(type(title)))
            urlencode_title = title # urllib.quote(title)
            mp3_url = response.request.meta['mp3_base'] + urlencode_title + '.mp3'
            #log.msg(mp3_url)

            # 发送mp3下载请求 refer: http://stackoverflow.com/questions/7123387/should-i-create-pipeline-to-save-files-with-scrapy
            req = Request(
                    url = mp3_url,
                    callback=self.download,
                    )
            req.meta['title'] = title
            req.meta['url'] = url
            req.meta['mp3_url'] = mp3_url

            result.append(req)

        return result

    def download(self, response):
        log.msg('download file content: %s' % str(response))

        item = JustingItem()
        item['title'] = response.request.meta['title']
        item['url'] = response.request.meta['url']
        item['mp3_url'] = response.request.meta['mp3_url']
        item['mp3_content'] = response.body

        return item

