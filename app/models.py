# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: models.py
@time: 2018/3/19 10:06
"""
import copy

from flask import json, app
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from . import db, login_manager


class Permission(object):
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=86400):
        s = Serializer(app.config.get('SECRET_KEY') or 'hello', expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config.get('SECRET_KEY') or 'hello')
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = User.query.get(data['id'])
        return user


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class MainTask(db.Model):
    __tablename__ = 'main_task'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    platform = db.Column(db.String(32))
    feature = db.Column(db.String(32))
    space = db.Column(db.Integer)
    headers = db.Column(db.String(1024))
    method = db.Column(db.String(8), default='GET')
    proxy = db.Column(db.String(8), default='HTTP')
    valid = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.Integer)


class Modules(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.Integer, primary_key=True)
    own = db.Column(db.String(16))
    platform = db.Column(db.String(32))
    feature = db.Column(db.String(32))
    package = db.Column(db.String(64))
    mould = db.Column(db.String(32))
    url = db.Column(db.String(1024))
    version = db.Column(db.String(16))
    file_md5 = db.Column(db.String(32))
    valid = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.Integer)
    __table_args__ = (UniqueConstraint('own', 'platform', 'feature', name='_own_platform_feature_uc'),)

    def update(self, new_modules):
        self.own = new_modules.own
        self.platform = new_modules.platform
        self.feature = new_modules.feature
        self.package = new_modules.package
        self.mould = new_modules.mould
        self.url = new_modules.url
        self.version = new_modules.version
        self.file_md5 = new_modules.file_md5
        self.valid = new_modules.valid
        self.timestamp = new_modules.timestamp
        db.session.commit()

    def to_dict(self):
        kws = copy.deepcopy(self.__dict__)
        del kws['_sa_instance_state']
        return kws
