# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: helper.py
@time: 2018/3/22 13:35
"""
import hashlib
import re

import time

from flask import json
from tddc import RedisClient

from .models import Modules
from client import app
from util.short_uuid import ShortUUID
from util.util import Singleton


def get_modules_info(platform, filename, data):
    modules = Modules()
    modules.platform = platform
    file_content = data.stream.getvalue()
    file_content = file_content.replace(' ', '')
    modules.package = filename.split('.')[0].split('/')[-1]
    ret = re.search(r'class(.*?)\(', file_content)
    if not ret and ret.groups():
        return None, 'Mould Not Found.(%s)' % filename
    modules.mould = ret.groups()[0]
    ret = re.search(r"version='(.*?)'", file_content)
    if not ret or not ret.groups():
        return None, 'Version Not Found.(%s)' % filename
    modules.version = ret.groups()[0]
    ret = re.search(r"feature='(.*?)'", file_content)
    if not ret and ret.groups():
        return None, 'Feature Not Found.(%s)' % filename
    modules.feature = ret.groups()[0]
    ret = re.search(r"valid='(.*?)'", file_content)
    valid = ret.groups()[0] if ret and ret.groups() else '1'
    modules.valid = valid == '1'
    _md5 = hashlib.md5()
    _md5.update(file_content)
    modules.file_md5 = _md5.hexdigest()
    modules.timestamp = int(time.time())
    return modules, ''


class EventPusher(RedisClient):

    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        nodes = [{'host': app.config['REDIS_NODE_HOST'],
                  'port': app.config['REDIS_NODE_PORT']}]
        super(EventPusher, self).__init__(startup_nodes=nodes, *args, **kwargs)

    def publish_event(self, channel, message):
        def _publish(_channel, _message):
            self.publish(_channel, _message)
        self.robust(_publish, channel, message)


def push_update_event(modules_info):
    event_id = ShortUUID.UUID()
    topic = 'tddc:event:{own}'.format(own=modules_info.own)
    data = {'e_type': 1001,
            'name': 'Modules Update',
            'describe': 'Modules(%s|%s) Update Event.' % (topic, modules_info.platform),
            'event': modules_info.to_dict(),
            'id': event_id,
            'status': 0,
            'timestamp': int(time.time())}
    EventPusher().publish_event(topic, json.dumps(data))
