class Product:
    def __init__(self, state):
        self.db = state['db']
        self.model = self.db['products']

    def get_products_for_category(self, category):
        return self.model.find({'category': category})
