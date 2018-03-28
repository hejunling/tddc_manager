# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: helper.py
@time: 2018/3/23 13:35
"""

import json
import logging
import time
import copy
import gevent

from tddc import StatusManager, RecordManager

from util.util import Singleton


log = logging.getLogger(__name__)


class ClientStatus(object):

    __metaclass__ = Singleton

    def __init__(self):
        super(ClientStatus, self).__init__()
        log.info('Client Status Monitor Is Starting..')
        self.exception_server_backup = {}
        gevent.spawn(self._monitor)
        gevent.sleep()
        log.info('Client Status Monitor Was ready.')

    def _monitor(self):
        while True:
            exception_server = {}
            clients = StatusManager().smembers('tddc:client:alive')
            status = StatusManager().get_all_status('tddc:status:client')
            cur_time = int(time.time())
            for client, state in status:
                if client not in clients:
                    continue
                state = json.loads(state)
                timeout = self._timeout_check(state, cur_time)
                if timeout:
                    exception_server[client] = timeout
                elif self.exception_server_backup.get(client):
                    del self.exception_server_backup[client]
            for client, exception in exception_server.items():
                if self.exception_server_backup.get(client) == exception:
                    continue
                # self.warning('Send Warning Email: [%s][%s]' % (client, exception))
                # EMailManager().send_mail('[TDDC Monitor] Server Exception',
                #                          json.dumps(exception_server, indent=4))
            self.exception_server_backup = copy.deepcopy(exception_server)
            time.sleep(5)

    @staticmethod
    def _timeout_check(state, cur_time):
        timeout = {}
        for server, timestamp in state.items():
            if cur_time - timestamp > 60:
                timeout[server] = timestamp
        return timeout

    @property
    def status(self):
        return self.exception_server_backup


class EventStatusMonitor(object):
    '''
    classdocs
    '''
    __metaclass__ = Singleton

    def __init__(self):
        '''
        Constructor
        '''
        self._status = {}
        super(EventStatusMonitor, self).__init__()
        log.info('Event Status Monitor Is Starting.')
        gevent.spawn(self._monitor)
        gevent.sleep()
        log.info('Event Status Monitor Was Started.')

    @property
    def status(self):
        return self._status

    def _monitor(self):
        while True:
            try:
                keys = StatusManager().keys('tddc:event:status:*')
                if not len(keys):
                    gevent.sleep(30)
                    continue
                platforms = [platform.split(':')[-1]
                             for platform in keys if len(platform.split(':')) == 4]
                processing_event_ids = {platform: StatusManager().smembers(
                    'tddc:event:status:processing:%s' % platform)
                                        for platform in platforms}
                processing_event_ids = {platform: ids
                                        for platform, ids in processing_event_ids.items()
                                        if len(ids)}
                if not len(processing_event_ids):
                    gevent.sleep(30)
                    continue
                statuses = {platform: {event_id: StatusManager().hgetall(
                    'tddc:event:status:value:' + event_id)
                                       for event_id in ids}
                            for platform, ids in processing_event_ids.items()}
                alive_worker = StatusManager().smembers('tddc:client:alive')
                result = self._status_check(statuses, alive_worker)
                # self._alarm(result)
                self._done(result)
            except Exception as e:
                print(e)
            gevent.sleep(30)

    def _status_check(self, statuses, alive_worker):
        cur_time = time.time()
        result = {}
        for platform, event_id_status in statuses.items():
            for event_id, worker_status in event_id_status.items():
                event_record = RecordManager().get_record('tddc:event:record:%s' % platform,
                                                          event_id)
                if not event_record:
                    print('Event(%s) Record Not Found.' % event_id)
                    return result
                event_record = type('EventRecord', (), json.loads(event_record))
                if cur_time - event_record.timestamp < 60:
                    continue
                for worker in alive_worker:
                    state = worker_status.get(worker, 'Timeout')
                    if state[-3:] == '200':
                        continue
                    if not result.get(platform, None):
                        result[platform] = {}
                    if not result[platform].get(event_id, None):
                        result[platform][event_id] = {}
                    result[platform][event_id][worker] = state
        return result

    def _alarm(self, status):
        if not len(status):
            return
        # EMailManager().send_mail('[TDDC Monitor] Event Exception',
        #                          json.dumps(status, indent=4))
        # self.warning(json.dumps(status,
        #                         indent=4))

    def _done(self, status):
        for platform, event_status in status.items():
            for event_id, _ in event_status.items():
                StatusManager().srem('tddc:event:status:processing:%s' % platform,
                                     event_id)
