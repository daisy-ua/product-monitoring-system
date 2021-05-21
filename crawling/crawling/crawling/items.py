import scrapy


class MichaelsProduct(scrapy.Item):
    item_id = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    price = scrapy.Field()
    currency = scrapy.Field()
    img_path = scrapy.Field()
    category = scrapy.Field()
    url = scrapy.Field()


class MichaelsCategory(scrapy.Item):
    _id = scrapy.Field()
    tree = scrapy.Field()
    parent = scrapy.Field()
