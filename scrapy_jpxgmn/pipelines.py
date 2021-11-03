# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymysql
from scrapy_jpxgmn.items import photoDataItem
from pymongo import MongoClient
import os


class ScrapyJpxgmnPipeline:
    # 保存文件到本地
    def process_item(self, item, spider):
        organization = item['organization']
        star = item['star']
        title = item['title']
        filename = item['img_url'].split('/')[-1]
        path = fr'F:\秀人系列\{organization}\{star}\{title}'
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        with open(filepath, mode='wb') as f:
            f.write(item['content'])
        return item


class photoData2MongodbPipeline:
    # 保存图片信息到mongodb
    def __init__(self, url, database, collection):
        self.url = url
        self.database = database
        self.collection = collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            url=crawler.settings.get('MONGO_URL'),
            database=crawler.settings.get('MONGO_DB'),
            collection=crawler.settings.get('MONGO_COLLECTION'),
        )

    def open_spider(self, spider):
        # 连接mysql
        self.client = MongoClient(self.url)
        self.database = self.client[self.database]
        self.collection = self.database[self.collection]

    def closer_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        insert_data = dict(item)
        insert_data['process'] = 0
        insert_data['local'] = 1
        try:
            self.collection.insert_one(insert_data)
        except Exception as e:
            print(e)
        return item


class photoData2MySqlPipeline:
    # 保存图片信息到mysql
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.keys = photoDataItem.fields.keys()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            port=crawler.settings.get('MYSQL_PORT'),
        )

    def open_spider(self, spider):
        # 连接mysql
        self.db = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port)
        self.cursor = self.db.cursor()

    def closer_spider(self, spider):
        self.db.close()

    def process_item(self, item, spider):
        photos_url = item['photos_url']
        # 写真的标题
        title = item['title']
        # 谁的写真
        star = item['star']
        # 机构
        organization = item['organization']
        # 写着描述
        photos_desc = item['photos_desc']
        # 写真有几页
        pages_nums = item['pages_nums']
        # 图片所在页面的地址
        photo_page_url = item['photo_page_url']
        # 图片的地址
        img_url = item['img_url']
        # 图片重定位的地址
        real_url = item['real_url']
        sql = "insert into data (photos_url,title,star,organization,photos_desc,pages_nums,photo_page_url,img_url," \
              "real_url) values ('%s', '%s', ' %s','%s', '%s',%s,'%s', '%s', '%s')" % (
                  photos_url, title, star, organization, photos_desc, pages_nums, photo_page_url, img_url, real_url)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(e)
        return item
