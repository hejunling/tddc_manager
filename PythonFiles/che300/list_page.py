# -*- coding: utf-8 -*-
'''
Created on 2017年4月13日

@author: chenyitao
'''

import time

from ..parse_rule_base import ParseRuleBase


class Che300ListPage(ParseRuleBase):
    '''
    classdocs
    '''

    platform = 'che300'

    feature = 'che300.list_page'

    version = '1495799988'

    def _parse(self):
        if self._xpath('//*[@class="active"]/a/text()')[0] == '1':
            self._make_want_buy_list_urls()
        self._make_detail_task()

    def _make_want_buy_list_urls(self):
        page_numbers = self._doc.xpath('//*[@class="pagination"]/span/text()')
        page_numbers = int(str(page_numbers[0].split(' ')[1]))
        for index in range(1, page_numbers):
            base_url = 'http://www.che300.com/buycar/?city=0&p=%d'
            url = base_url % (20 * index)
            task = Task()
            task.url = url
            task.platform = self.platform
            task.feature = self.feature
            task.headers = None if index == 1 else {'Referer': base_url % (20*index-1),
                                                    'Set-Cookie': self._task.headers.get('Set-Cookie')}
            self._md5_mk.update(url)
            task.row_key = self._md5_mk.hexdigest()
            self.tasks.append(task)

    def _make_detail_task(self):
        detail_urls = self._xpath('//*[@class="list-item"]/a/@href')
        for url in detail_urls:
            task = Task()
            task.url = url.replace('https', 'http')
            task.platform = self.platform
            task.feature = 'che300.deatil'
            task.headers = {'Referer': self._task.url,
                            'Set-Cookie': self._task.headers.get('Set-Cookie')}
            self._md5_mk.update(task.url)
            task.row_key = self._md5_mk.hexdigest()
            self.tasks.append(task)