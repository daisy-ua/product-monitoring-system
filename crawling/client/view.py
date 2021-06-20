from crawling.crawling.spiders.michaels import run
from client.controllers.controller import Controller

GENERATE_DATA = 1
GET_PRODUCTS = 2
START_ANALYSIS = 3
BACK = 0

menu_option = [
    '1. start scrapy',
    '2. get products',
    '3. start analysis',
    '0. quit'
]


class View:
    def __init__(self, state):
        self.state = state
        self.controller = Controller(state)

    def show(self):
        while True:
            print_initial(menu_option)
            option = int(input("----> "))

            if option == GENERATE_DATA:
                run()

            if option == GET_PRODUCTS:
                self.get_categories_menu(self.get_products)

            if option == START_ANALYSIS:
                self.start_analysis()

            if option == BACK:
                break

    def get_products(self, category_name):
        products = self.controller.get_all_products_for_category(category_name)

        if len(products) == 0:
            print_message('No products found for this category!')
            return None
        print_enumerated_list(products, 'name')
        return products

    def get_categories_menu(self, callback):
        categories = self.controller.get_parent_categories()
        while True:
            print_message('Select category. Press 0 to exit!')
            print_enumerated_list(categories, '_id')

            option = int(input('----> '))

            if option == BACK:
                break

            if option > len(categories):
                print_message("Out of index! Try again.")
                continue

            category_name = categories[option - 1]['_id']
            sub_categories = self.controller.get_parent_categories(category_name)
            if len(sub_categories) != 0:
                categories = sub_categories
                continue

            return callback(category_name)

    def start_analysis(self):
        menu = [
            '1. get category ranking by sales',
            '2. get average prices for category',
            '3. get price prediction',
            '0. back'
        ]

        while True:
            print_initial(menu, 'Select analysis option')
            option = int(input('----> '))

            if option == 1:
                self.get_category_ranking()

            if option == 2:
                self.get_categories_menu(self.get_average_prices_by_category)

            if option == 3:
                self.get_price_prediction()

            if option == BACK:
                break

    def get_category_ranking(self):
        self.controller.get_category_ranking()

    def get_average_prices_by_category(self, category_name):
        if self.controller.get_average_prices_by_category(category_name):
            print('Success!')

    def get_price_prediction(self):
        products = self.get_categories_menu(self.get_products)
        if products is None:
            return
        option = int(input('----> '))
        if self.controller.get_price_prediction(products[option - 1]['item_id']):
            print('Success!')


def print_enumerated_list(items, key):
    for count, item in enumerate(items):
        print(f"{Colors.WHITE}%i. %s" % (count + 1, item[key]))


def print_message(message):
    print(f"{Colors.YELLOW}%s" % message)


def print_initial(options, message="\nSelect option to continue:"):
    print_message(message)
    for item in options:
        print(f"{Colors.WHITE}%s" % item)


class Colors:
    YELLOW = "\033[38;5;208m"
    WHITE = "\033[38;5;231m"
    RED = "\033[31m"
    GREEN = "\033[32m"
