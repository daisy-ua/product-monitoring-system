import pymongo
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import DropItem
from .items import MichaelsProduct, MichaelsCategory
from crawling.crawling.generator import generate_sale_history


class MongoDBPipeline(object):

    def __init__(self):
        settings = get_project_settings()
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.products = db[settings['MONGODB_PRODUCT_COLLECTION']]
        self.categories = db[settings['MONGODB_CATEGORY_COLLECTION']]
        self.sales = db[settings['MONGODB_SALES_COLLECTION']]

    def close_spider(self, spider):
        for product in self.products.find():
            sales = generate_sale_history(product['item_id'], product['price'])
            self.sales.find_one_and_update({'_id': product['item_id']}, {'$set': dict(sales)}, upsert=True)

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        if isinstance(item, MichaelsCategory):
            self.__process_category_item(item)

        if isinstance(item, MichaelsProduct) and item['item_id'] is not None:
            self.__process_product_item(item)

        return item

    def __process_category_item(self, item):
        self.categories.update({'_id': item['_id']}, {'$set': dict(item)}, upsert=True)

    def __process_product_item(self, item):
        product = self.products.find_one({'item_id': item['item_id']})
        if not product:
            self.products.insert_one(dict(item))
            return
        if product['category'] != item['category']:
            product['category'] += item['category']
        self.products.update_one({'item_id': item['item_id']}, {'$set': dict(product)}, upsert=True)
