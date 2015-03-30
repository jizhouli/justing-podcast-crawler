# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys

from scrapy import log
from scrapy.exceptions import DropItem

class JustingPipeline(object):
    def process_item(self, item, spider): #pylint:disable=unused-argument
        return item

class ValidatePipeline(object):
    def process_item(self, item, spider): # #pylint:disable=unused-argument
        if item['title']:
            log.msg("ValidatePipeline - valide item: %s" % str(item))
            return item
        else:
            raise DropItem("ValidatePipeline - title is empty: %s" % str(item))

class StoreToFilePipeline(object):
    def process_item(self, item, spider): #pylint:disable=unused-argument
        path = './download/' + item['title'] + '.mp3'
        #log.msg(self.cur_file_dir() + '/' + path)
        with open(path, 'wb') as f:
            f.write(item['mp3_content'])
        del item['mp3_content']
        return item

    def cur_file_dir(self):
        path = sys.path[0]
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)
