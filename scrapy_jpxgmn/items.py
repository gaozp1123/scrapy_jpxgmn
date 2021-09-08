# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyXiurenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class photoDataItem(scrapy.Item):
    # 写真的url地址
    photos_url = scrapy.Field()
    # 写真的标题
    title = scrapy.Field()
    # 谁的写真
    star = scrapy.Field()
    # 机构
    organization = scrapy.Field()
    # 写着描述
    photos_desc = scrapy.Field()
    # 写真有几页
    pages_nums = scrapy.Field()
    # 图片所在页面的地址
    photo_page_url = scrapy.Field()
    # 图片的地址
    img_url = scrapy.Field()
    # 写真的内容
    content = scrapy.Field()
    # 图片重定位的地址
    real_url = scrapy.Field()
