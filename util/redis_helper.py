# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: redis_client.py
@time: 2018/3/23 13:36
"""
import time
from rediscluster import StrictRedisCluster

from util import Singleton


class RedisClient(StrictRedisCluster):
    '''
    classdocs
    '''

    def __init__(self, *args, **kwargs):
        super(RedisClient, self).__init__(max_connections=64, *args, **kwargs)

    def robust(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            print('Try Again.')
            if self.connection_pool._created_connections != 0:
                self.connection_pool.reset()
            time.sleep(2)
            return self.robust(func, *args, **kwargs)

    def clean(self, pattern='*'):
        def _clean(_pattern):
            for key in self.keys(pattern):
                self.delete(key)
            else:
                return True
        return self.robust(_clean, pattern)


class StatusManager(RedisClient):

    __metaclass__ = Singleton

    def __init__(self):
        from client import app
        nodes = [{'host': app.config['REDIS_NODE_HOST'],
                  'port': app.config['REDIS_NODE_PORT']}]
        super(StatusManager, self).__init__(startup_nodes=nodes)

    def get_status(self, name, key):
        def _get_status(_name, _key):
            return self.hget(_name, _key)

        return self.robust(_get_status, name, key)

    def update_status(self, name, key, new_status, old_status=None):
        def _update_status(_name, _key, _new_status, _old_status):
            self.hmove((_name + ':' + str(_old_status)) if _old_status is not None else None,
                       _name + ':' + str(_new_status),
                       _key,
                       str(int(time.time())))

        self.robust(_update_status, name, key, new_status, old_status)

    def set_status(self, name, key, status):
        def _set_status(_name, _key, _status):
            self.hset(_name, key, _status)

        self.robust(_set_status, name, key, status)

    def set_multi_status(self, name, status):
        def _set_multi_status(_name, _status):
            self.hmset(_name, _status)

        self.robust(_set_multi_status, name, status)

    def get_all_status(self, name):
        def _get_all_status(_name):
            return self.hscan_iter(_name)

        return self.robust(_get_all_status, name)


class RecordManager(RedisClient):
    '''
    classdocs
    '''
    __metaclass__ = Singleton

    def __init__(self):
        from client import app
        nodes = [{'host': app.config['REDIS_NODE_HOST'],
                  'port': app.config['REDIS_NODE_PORT']}]
        super(RecordManager, self).__init__(startup_nodes=nodes)

    def create_record(self, name, key, record):
        def _create_record(_name, _key, _record):
            self.hset(_name, _key, _record)
        self.robust(_create_record, name, key, record)

    def create_records(self, name, records):
        def _create_records(_name, _records):
            self.hmset(_name, _records)
        self.robust(_create_records, name, records)

    def get_record_sync(self, name, key, callback, **kwargs):
        def _get_record_sync(_name, _key, _callback, **_kwargs):
            record = self.hget(_name, _key)
            _callback(record, **_kwargs)
        self.robust(_get_record_sync, name, key, callback, **kwargs)

    def get_record(self, name, key):
        def _get_record_sync(_name, _key):
            return self.hget(_name, _key)
        return self.robust(_get_record_sync, name, key)
