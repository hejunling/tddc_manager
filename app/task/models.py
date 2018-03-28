# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: models.py
@time: 2018/3/27 20:06
"""
import copy

from app import db


class TaskConfigModel(db.Model):
    __tablename__ = 'task_config'

    id = db.Column(db.Integer, primary_key=True)
    crawler_topic = db.Column(db.String(32))
    parser_topic = db.Column(db.String(32))
    cache_key_base = db.Column(db.String(32))
    status_key_base = db.Column(db.String(32))
    record_key_base = db.Column(db.String(32))
    max_queue_size = db.Column(db.Integer)


class MainTask(db.Model):
    __tablename__ = 'main_task'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024))
    platform = db.Column(db.String(32))
    feature = db.Column(db.String(32))
    status = db.Column(db.Integer)
    space = db.Column(db.Integer)
    headers = db.Column(db.String(1024))
    method = db.Column(db.String(8), default='GET')
    proxy = db.Column(db.String(8), default='HTTP')
    valid = db.Column(db.Boolean, default=True)
    timestamp = db.Column(db.Integer)

    def to_dict(self):
        kws = copy.deepcopy(self.__dict__)
        del kws['_sa_instance_state']
        return kws
