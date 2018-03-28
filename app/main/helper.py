# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: helper.py
@time: 2018/3/24 14:04
"""
import logging
import gevent
import psutil
import time

from flask import json
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import SystemResourceModel
from util.util import Singleton


log = logging.getLogger(__name__)


class SystemResourceMonitor(object):

    __metaclass__ = Singleton

    def __init__(self):
        log.info('System Resource Monitor Starting.')
        from client import app
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                               pool_recycle=3600, echo=False)
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()
        gevent.spawn(self._monitor)
        gevent.sleep()
        log.info('System Resource Monitor Was Ready.')

    def _monitor(self):
        while True:
            gevent.sleep(10)
            srm = SystemResourceModel()
            srm.cpu_count = psutil.cpu_count()
            srm.cpu_used_percent = json.dumps(psutil.cpu_percent(percpu=True))
            mem = psutil.virtual_memory()
            srm.mem_total = mem.total
            srm.mem_used_percent = mem.percent
            srm.timestamp = int(time.time())
            self.session.add(srm)
            self.session.commit()
            gevent.sleep(50)

    def last_24_hour_used(self):
        return SystemResourceModel.query.filter(SystemResourceModel.timestamp > (time.time() - 86400)).all()
