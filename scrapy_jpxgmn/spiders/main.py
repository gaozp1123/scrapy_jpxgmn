from scrapy.spiders import Spider
from scrapy_jpxgmn.items import photoDataItem
from scrapy import Request


class downloadspider(Spider):
    name = 'main'
    start_urls = ['https://www.jpxgmn.top/']

    def parse(self, response):
        # organization = response.xpath('//div[@class="sitenav"]/ul/li[2]/ul/li/a/@href').getall()
        yield from response.follow_all(xpath='//div[@class="sitenav"]/ul/li[2]/ul/li/a', dont_filter=True, callback=self.parse_photos_page)

    def parse_photos_page(self, response):
        yield from response.follow_all(xpath='//li[@class="related_box"]/a', dont_filter=True, callback=self.parse_photos)
        next = response.xpath(
            '//div[@class="pagination"]//a[text()="下一页"]/@href').get()
        if next is not None:
            yield response.follow(next, dont_filter=True, callback=self.parse_photos_page)

    def parse_photos(self, response):
        item = photoDataItem()
        item['photos_url'] = response.url
        item['title'] = response.xpath(
            '//h1[@class="article-title"]/text()').get()
        item['star'] = response.xpath(
            '//span[@class="item item-2"]/a/text()').get()
        item['organization'] = response.xpath(
            '//div[@class="toptip"]/a[2]/text()').get()
        item['photos_desc'] = response.css(
            '.article-meta').xpath('./span[@class="item item-5"]/text()').getall()[-1]
        pages = response.xpath(
            '//div[@class="pagination"][1]/ul/a/@href')[1:-1]
        item['pages_nums'] = len(pages) + 1
        for page in pages:
            yield response.follow(page, callback=self.parse_nextpage, meta=item)
        item['photo_page_url'] = response.url
        photo_urls = response.xpath(
            '//img[@onload="size(this)"]/@src').getall()
        for url in photo_urls:
            photo_url = response.urljoin(url)
            item['img_url'] = photo_url
            yield Request(photo_url, callback=self.parse_photo, dont_filter=True, meta=item)

    def parse_nextpage(self, response):
        item = response.meta
        photo_urls = response.xpath(
            '//img[@onload="size(this)"]/@src').getall()
        item['photo_page_url'] = response.url
        for url in photo_urls:
            photo_url = response.urljoin(url)
            item['img_url'] = photo_url
            yield Request(photo_url, callback=self.parse_photo, meta=item)

    def parse_photo(self, response):
        item = response.meta
        item['real_url'] = response.url
        item['content'] = response.body
        yield item
