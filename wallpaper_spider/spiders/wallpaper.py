import scrapy
from urllib.parse import urljoin
import re
from ..items import WallpaperSpiderItem


class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    start_url = 'http://qianye88.com'

    def start_requests(self):
        yield scrapy.Request(url=self.start_url, callback=self.category_parse)

    # 解析壁纸分类
    def category_parse(self, response):
        category_urls = response.css('.category a::attr(href)').getall()
        category_names = response.css('.category a::text').getall()
        for index, url in enumerate(category_urls):
            category_url = urljoin(response.url, url)
            classify = re.sub(r'(\d(k|K))', '', category_names[index])
            yield scrapy.Request(url=category_url, callback=self.list_parse, meta={'classify': classify})

    # 解析壁纸列表
    def list_parse(self, response):
        detail_urls = response.css('.flex-images .item a.image::attr(href)').getall()
        for url in detail_urls:
            detail_url = urljoin(response.url, url)
            yield scrapy.Request(url=detail_url, callback=self.detail_parse, meta=response.meta)

    # 解析壁纸详情
    def detail_parse(self, response):
        item = WallpaperSpiderItem()
        item['id'] = response.css('.content-info span:nth-child(1)::text').get().split('：')[-1]
        item['url'] = response.css('.content-img::attr(src)').get().split('?')[0]
        title = response.css('.content-title::text').get()
        item['title'] = re.sub(r'(\d(k|K))|(\d+x\d+)|(超?高?清)|背景|壁纸|图片', '', title)
        item['classify'] = response.meta['classify']
        description = response.css('.content-desc::text').get()
        item['time'] = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', description).group()
        print('\n*******************\n', item, '\n*******************\n')
