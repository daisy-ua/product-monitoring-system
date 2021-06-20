class History:
    def __init__(self, state):
        self.db = state['db']
        self.model = self.db['sales']

    def get_cursor(self):
        return self.model.find({})
