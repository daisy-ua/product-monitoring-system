import shlex
from subprocess import Popen

from pymongo import MongoClient
from scrapy.utils.project import get_project_settings
from client.view import View


def backup(_host, _port):
    try:
        cmd = shlex.split('mongodump --host %s --port %i --out  /var/lib/mongodb/data/backup' % (_host, int(_port)))
        p = Popen(cmd)
        p.wait()
    except AssertionError:
        print('Failed to backup.')


if __name__ == '__main__':
    settings = get_project_settings()
    client = MongoClient(
        settings['MONGODB_SERVER'],
        settings['MONGODB_PORT']
    )
    db = client['catalog']
    state = {'db': db}

    View(state).show()

    backup(client.HOST, client.PORT)
