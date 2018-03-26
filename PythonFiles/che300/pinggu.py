# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author: chenyitao
'''

import time

from ..parse_rule_base import ParseRuleBase


class Che300PingguPage(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'che300'

    feature = 'che300.pinggu'

    version = '1495799988'

    def _parse(self):
        self._make_pinggu_task()

    def _make_pinggu_task(self):
        pinggu = self._xpath('//*[@class="sp-strong"]')
        TDDCLogging.info('che300.pinggu %s.' % ('Successed' if pinggu else 'Failed'))