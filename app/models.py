# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: models.py
@time: 2018/3/19 10:06
"""
from . import db


class RedisConfigModel(db.Model):
    __tablename__ = 'redis_config'

    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String)
    port = db.Column(db.Integer)
    user = db.Column(db.String)
    passwd = db.Column(db.String)
    db = db.Column(db.String)
