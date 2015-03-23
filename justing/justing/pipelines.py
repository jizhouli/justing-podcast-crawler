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
        if item['title']:
            log.msg("ValidatePipeline - valide item: %s" % str(item))
            return item
        else:
            raise DropItem("ValidatePipeline - title is empty: %s" % str(item))
