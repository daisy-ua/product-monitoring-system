from iteration_utilities import unique_everseen
from client.models.category import Category
from client.models.product import Product


class Controller:
    def __init__(self, state):
        self.category = Category(state)
        self.product = Product(state)

    def get_all_items(self):
        return self.category.get_all_items()

    def get_all_products_for_category(self, parent):
        products = list(self.product.get_products_for_category(parent))
        categories = self.category.get_descendants_items(parent)
        for category in categories:
            products += self.product.get_products_for_category(category['_id'])
        return list(unique_everseen(products))
