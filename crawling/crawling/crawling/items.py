# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MichaelsProduct(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    img_path = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()


