from client.controllers.controller import Controller

GENERATE_DATA = 1
GET_PRODUCTS = 2
BACK = 0

menu_option = [
    '1. start scrapy',
    '2. get products',
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
                pass

            if option == GET_PRODUCTS:
                self.get_products_menu()

            if option == BACK:
                break

            continue

    def get_products_menu(self):
        while True:
            categories = list(self.controller.get_all_items())
            print_message('Select category. Press 0 to exit!')
            print_enumerated_list(categories, '_id')

            option = int(input('----> '))

            if option > len(categories):
                print_message("Out of index! Try again.")
                continue

            if option == BACK:
                break

            category_name = categories[option - 1]['_id']
            products = self.controller.get_all_products_for_category(category_name)

            if len(products) == 0:
                print_message('No products found for this category!')
            print_enumerated_list(products, 'name')

            break


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
