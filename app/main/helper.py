# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: helper.py
@time: 2018/3/24 14:04
"""
import threading

import copy
import gevent
import psutil
import time

from flask import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from app import db
from util.util import Singleton


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


class SystemResourceMonitor(object):

    __metaclass__ = Singleton

    def __init__(self):
        threading.Thread(target=self._monitor).start()

    def _monitor(self):
        from client import app
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                               pool_recycle=3600, echo=False)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        while True:
            time.sleep(10)
            srm = SystemResourceModel()
            srm.cpu_count = psutil.cpu_count()
            srm.cpu_used_percent = json.dumps(psutil.cpu_percent(percpu=True))
            mem = psutil.virtual_memory()
            srm.mem_total = mem.total
            srm.mem_used_percent = mem.percent
            srm.timestamp = int(time.time())
            session.add(srm)
            session.commit()
            # time.sleep(50)

    def last_24_hour_used(self):
        return SystemResourceModel.query.filter(SystemResourceModel.timestamp > (time.time() - 86400)).all()
