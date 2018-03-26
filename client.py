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

from gevent.monkey import patch_all
from werkzeug.contrib.fixers import ProxyFix

from gevent.wsgi import WSGIServer
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell

from app import create_app, db
from app.models import User, MainTask, Modules

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
app.wsgi_app = ProxyFix(app.wsgi_app)
migrate = Migrate(app, db)
manager = Manager(app)


def make_shell_context():
    return dict(db=db, User=User, MainTask=MainTask, Modules=Modules)


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    # patch_all()
    # http_server = WSGIServer(('', 5005), app)
    # http_server.serve_forever()
    manager.add_command('shell', Shell(make_context=make_shell_context))
    manager.add_command('db', MigrateCommand)
    manager.run()
