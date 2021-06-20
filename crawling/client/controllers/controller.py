from iteration_utilities import unique_everseen
from client.models.category import Category
from client.models.product import Product
from client.models.history import History
import analysis.analysis as analysis


class Controller:
    def __init__(self, state):
        self.category = Category(state)
        self.product = Product(state)
        self.history = History(state)

    def get_all_items(self):
        return self.category.get_all_items()

    def get_category_db(self):
        return list(self.category.get_all_items())

    def get_all_products_for_category(self, parent):
        products = list(self.product.get_products_for_category(parent))
        categories = self.category.get_descendants_items(parent)
        for category in categories:
            products += self.product.get_products_for_category(category['_id'])
        return list(unique_everseen(products))

    def get_parent_categories(self, parent='root'):
        return list(self.category.get_parent_nodes(parent))

    def get_average_prices_by_category(self, category):
        analysis.get_average_prices_by_category(list(self.history.get_cursor()),
                                                list(self.product.get_cursor()),
                                                category)

    def get_category_ranking(self):
        analysis.get_category_ranking(list(self.history.get_cursor()),
                                      list(self.product.get_cursor()))

    def get_price_prediction(self, product_id):
        analysis.get_price_prediction(product_id, self.history.get_cursor())
