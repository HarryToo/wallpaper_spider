# -*- coding: utf-8 -*-

import scrapy


class WallpaperSpiderItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    classify = scrapy.Field()
    size = scrapy.Field()
    volume = scrapy.Field()
    time = scrapy.Field()
