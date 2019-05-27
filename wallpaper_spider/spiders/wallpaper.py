import scrapy
from ..items import WallpaperSpiderItem


class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    start_url = 'http://qianye88.com'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.parse)

    def parse(self, response):
        category = response.css('.category a::text').getall()
        print(category)
