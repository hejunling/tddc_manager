# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: helper.py
@time: 2018/3/27 19:47
"""

import logging

import gevent
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import MainTask
from app.task.models import TaskConfigModel

logging.getLogger('PIL').setLevel(logging.WARN)
from tddc import (Singleton, TaskManager, Task, TaskRecordManager)

log = logging.getLogger(__name__)


class TaskCenter(object):
    __metaclass__ = Singleton

    def __init__(self):
        log.info('Task Center Starting.')
        super(TaskCenter, self).__init__()
        from client import app
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                               pool_recycle=3600, echo=False)
        Session = scoped_session(sessionmaker(bind=engine))
        self.session = Session()
        self.task_config = self.session.query(TaskConfigModel).get(1)
        self._status = {}
        gevent.spawn(self._main_task_manager)
        gevent.sleep()
        gevent.spawn(self._task_recycle)
        gevent.sleep()
        log.info('Task Center Was Ready.')

    def _main_task_manager(self):
        """
        Get Task Info From Redis
        :return:
        """
        self.main_tasks_id = set()
        while True:
            try:
                self._fetch_main_task()
            except Exception as e:
                log.exception(e)
                log.warning(e.message)
            gevent.sleep(30)

    def _fetch_main_task(self):
        tasks = self.session.query(MainTask).all()
        cur_time = int(time.time())
        for task in tasks:
            if not task.valid or ((cur_time - float(task.timestamp)) < float(task.space)):
                continue
            task.timestamp = cur_time
            task.status = Task.Status.CrawlTopic
            TaskRecordManager().create_record(task)
            TaskManager('manager').push_task(task, self.task_config.crawler_topic)
            self.session.add(task)
        self.session.commit()

    def _task_recycle(self):
        for event in TaskRecordManager().psubscribe('__keyevent@0__:*'):
            log.info(event)
            if event.get('type') == 'psubscribe':
                continue
            task_index = event.get('data')
            task_index = ':'.join(task_index.split(':')[:-1])
            task = TaskRecordManager().get_records(task_index)
            if not task:
                continue
            task.status = Task.Status.CrawlTopic
            TaskManager('manager').push_task(task, self.task_config.crawler_topic)
