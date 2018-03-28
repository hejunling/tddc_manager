# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: client.py
@time: 2018/3/20 17:54
"""
import os

import logging

from gevent.monkey import patch_all
from werkzeug.contrib.fixers import ProxyFix

from gevent.wsgi import WSGIServer
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.auth.models import User
from app.modules.models import Modules

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.wsgi_app = ProxyFix(app.wsgi_app)
migrate = Migrate(app, db)
manager = Manager(app)

logging.getLogger('PIL').setLevel(logging.WARN)
log = logging.getLogger(__name__)


def make_shell_context():
    return dict(db=db, User=User, Modules=Modules)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


def start_plugin():
    from app.task.helper import TaskCenter
    TaskCenter()
    from app.monitor.helper import ClientStatus, EventStatusMonitor
    ClientStatus()
    EventStatusMonitor()
    from app.main.helper import SystemResourceMonitor
    SystemResourceMonitor()


if __name__ == '__main__':
    # shell = True
    shell = False
    if not shell:
        patch_all()
        start_plugin()
        host = '0.0.0.0'
        port = 5001
        http_server = WSGIServer((host, port), app)
        log.info('Server(http://{}:{}) Starting.'.format(host, port))
        http_server.serve_forever()
    else:
        manager.add_command('shell', Shell(make_context=make_shell_context))
        manager.add_command('db', MigrateCommand)
        manager.run()
