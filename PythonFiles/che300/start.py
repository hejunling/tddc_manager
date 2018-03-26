# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author: chenyitao
'''
import json
import time

# from tddc.common.models import Task
# from tddc.common import TDDCLogging

from ..parse_rule_base import ParseRuleBase


class Che300StartPage(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'che300'

    feature = 'che300.start'

    version = '1495799988'

    def _parse(self):
        self._make_pinggu_task()

    def _make_pinggu_task(self):
        with open('./che300.json') as f:
            pg_list = [kv.get('model_url') for kv in json.loads(f.read())]
        for url in pg_list:
            pass
            # task = Task()
            # task.url = url
            # task.platform = self.platform
            # task.feature = 'che300.pg'
            # self._md5_mk.update(url)
            # task.row_key = self._md5_mk.hexdigest()
            # self.tasks.append(task)
