# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: models.py
@time: 2018/3/28 17:40
"""
import copy
import json

from app import db


class SystemResourceModel(db.Model):
    __tablename__ = 'system_resource_used'

    id = db.Column(db.Integer, primary_key=True)
    cpu_count = db.Column(db.Integer)
    cpu_used_percent = db.Column(db.Text)
    mem_total = db.Column(db.BigInteger)
    mem_used_percent = db.Column(db.Float(2))
    net_send_total = db.Column(db.BigInteger)
    net_recv_total = db.Column(db.BigInteger)
    net_upstream = db.Column(db.Integer)
    net_downstream = db.Column(db.Integer)
    timestamp = db.Column(db.Integer)

    def cpu_used_percent_list(self):
        return json.loads(self.cpu_used_percent)

    def to_dict(self):
        kws = copy.deepcopy(self.__dict__)
        kws['cpu_used_percent'] = self.cpu_used_percent_list()
        del kws['_sa_instance_state']
        return kws
