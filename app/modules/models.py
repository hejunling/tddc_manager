# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: models.py
@time: 2018/3/28 17:42
"""
import copy

from migrate import UniqueConstraint

from app import db


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
