class Category:
    def __init__(self, state):
        self.db = state['db']
        self.model = self.db['categories']

    def get_all_items(self):
        return self.model.find({}, {'_id': 1})

    def get_descendants_items(self, parent_node):
        return self.model.find({'tree': parent_node})



