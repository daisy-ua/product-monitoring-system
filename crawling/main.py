from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from client.view import View


if __name__ == '__main__':
    settings = get_project_settings()
    client = MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    db = client['catalog']
    state = {'db': db}

    View(state).show()
