# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/19 09:59
"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, patch_request_class
from flask_wtf import CSRFProtect

from config import config
from monkey_patch import patch_all

bootstrap = Bootstrap()
migrate = Migrate()
csrf = CSRFProtect()
moment = Moment()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
db = SQLAlchemy()
upload_set = None


def create_app(config_name):
    patch_all()
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    csrf.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    global upload_set
    upload_set = UploadSet('PythonFiles',
                           extensions=app.config.get('UPLOADS_MYFILE_ALLOW'))
    configure_uploads(app, upload_set)
    patch_request_class(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .modules import modules as modules_blueprint
    app.register_blueprint(modules_blueprint, url_prefix='/modules')

    from .task import task as task_blueprint
    app.register_blueprint(task_blueprint, url_prefix='/task')

    from .monitor import monitor as monitor_blueprint
    app.register_blueprint(monitor_blueprint, url_prefix='/monitor')

    from .wedis import wedis as wedis_blueprint
    app.register_blueprint(wedis_blueprint, url_prefix='/wedis')

    return app
