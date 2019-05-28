# -*- coding: utf-8 -*-

import time
from hashlib import sha1
import qiniu
import pymysql

oss_domain = 'http://ps7imii2c.bkt.clouddn.com'
access_key = 'HonIPmTV8Pchc_45LjX9l9Zq6DqeQ8BdG3HSbIRI'
secret_key = '8GUCriTpXtmaoPVkCAoMpB5G-OvIjfrVOUi1Ue0p'
bucket_name = 'wallpaper'
q = qiniu.Auth(access_key, secret_key)
bucket = qiniu.BucketManager(q)
connect = pymysql.connect(host="localhost", db="spider", user="root", passwd="123456", charset='utf8', use_unicode=True,
                          cursorclass=pymysql.cursors.DictCursor)
cursor = connect.cursor()


# 保存到OSS
class OssPipeline(object):
    def process_item(self, item, spider):
        extension = item['url'].split('.')[-1]
        key = '%s/%s_%s.%s' % (item['classify'], item['title'], int(time.time()), extension)
        ret, info = bucket.fetch(item['url'], bucket_name, key)
        base_url = '%s/%s' % (oss_domain, key)
        item['url'] = q.private_download_url(base_url, expires=3600)
        print('\n*******************\n', item, '\n*******************\n')
        return item


# 数据入库
class SqlPipeline(object):
    def process_item(self, item, spider):
        return item


# 保存爬取进度
class SchedulePipeline(object):
    def process_item(self, item, spider):
        return item
