# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sys
import traceback

from scrapy import log
from scrapy.exceptions import DropItem

class JustingPipeline(object):
    def process_item(self, item, spider):
        return item

class ValidatePipeline(object):
    def process_item(self, item, spider):
        log.msg("In ValidatePipeline", level=log.WARNING)        
        if item['title']:
            return item
        else:
            raise DropItem("title is empty")
