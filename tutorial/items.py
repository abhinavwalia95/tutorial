# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class blos_categ_Item(scrapy.Item):
    categ_name=scrapy.Field()
    categ_link=scrapy.Field()

class blos_list_categ_Item(scrapy.Item):
    categ_item_name=scrapy.Field()
    categ_item_author=scrapy.Field()

