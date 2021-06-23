import os

import scrapy
from subprocess import Popen
import shlex

from ..items import MichaelsProduct, MichaelsCategory


def parse_product(response):
    item = MichaelsProduct()
    item['item_id'] = response.meta['data-id']
    item['name'] = response.xpath("//h1[@class = 'product-name clearfix']/text()").get()
    price_item = str(response.xpath("//div[contains(@class, 'product-sales-price')]/text()").get()).strip()
    item['price'] = price_item[1:].replace(',', '')
    item['currency'] = price_item[0]
    item['desc'] = str(response.xpath("//div[@class='productshortDescriptions ']/text()").get()).strip()
    item['img_path'] = response.xpath("//div[@id='gal_01']/a/img/@src").get()
    item['category'] = response.meta['category-path']
    item['url'] = response.url
    yield item


class MichaelsSpider(scrapy.Spider):
    name = 'michaels'
    allowed_domains = ['michaels.com']
    start_urls = ['https://www.michaels.com/shop-categories/decor/974732331']
    domain = 'https://www.michaels.com'
    counter = 0

    def parse(self, response):
        category_links = response.xpath("//ul[@class='subcat category-level-1 ']/li/a")
        try:
            for category in category_links:
                category_name = str(category.xpath('.//text()').get()).strip()
                link = category.xpath(".//@href").get()
                absolute_path = self.domain + link

                category_node = MichaelsCategory()
                category_node['parent'] = "root"
                category_node['tree'] = ['root']
                category_node['_id'] = category_name
                yield category_node

                yield scrapy.Request(absolute_path, callback=self.parse_subcategory, meta={
                    'level': '2',
                    'category-path': [category_name],
                    'category-node': category_node
                })
        except Exception as err:
            print('Exception occurred: {0}'.format(err))

    def parse_subcategory(self, response):
        level = response.meta['level']
        categories = response.xpath("//ul[contains(@class, 'category-level-%s')]/li/a" % level)

        if categories:
            category_node = response.meta['category-node']
            category_node['parent'] = category_node['_id']
            category_node['tree'] += [category_node['_id']]

            for category in categories:
                name = str(category.xpath(".//text()").get()).strip()
                link = category.xpath(".//@href").get()
                if self.domain in link:
                    absolute_path = link
                else:
                    absolute_path = self.domain + link

                yield scrapy.Request(absolute_path, self.parse_subcategory, meta={
                    'level': str(int(level) + 1),
                    'category-path': name,
                    'category-node': category_node
                })

                category_node['_id'] = name
                yield category_node
        else:
            for page in self.parse_product_page(response):
                yield page

    def parse_product_page(self, response):
        cards = response.xpath("//div[@class='product-tile']")
        for card in cards:
            link = card.xpath(".//div[1]/a/@href").get()
            absolute_path = self.domain + link
            data_id = card.xpath(".//@data-itemid").get()
            response.meta['data-id'] = data_id
            yield scrapy.Request(absolute_path, callback=parse_product, meta=response.meta)

        next_page_link = response.xpath("//ul/div[@class='mobile_pagination']/a[@class='page-next']/@href").get()
        if next_page_link:
            yield scrapy.Request(next_page_link, callback=self.parse_product_page, meta=response.meta)


def run():
    settings_file_path = 'crawling.crawling.settings'
    os.environ.setdefault('SCRAPY_SETTINGS_MODULE', settings_file_path)
    cmd = shlex.split('scrapy crawl michaels')
    p = Popen(cmd)
    p.wait()

