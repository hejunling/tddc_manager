# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: views.py
@time: 2018/3/21 10:54
"""
from collections import defaultdict

import time
from flask import render_template
from flask_login import login_required

from app.monitor.helper import ClientStatus, EventStatusMonitor
from . import monitor


@monitor.route('/status/client')
@login_required
def client_status():
    status = ClientStatus().status
    result = defaultdict(dict)
    for k, v in status.items():
        own, hostname = k.split('|')
        for service, ts in v.items():
            time_array = time.localtime(ts)
            date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
            v[service] = date
        result[own][hostname] = v
    return render_template('monitor/client_status.html', status=result)


@monitor.route('/status/event')
@login_required
def event_status():
    status = EventStatusMonitor().status
    return render_template('monitor/event_status.html')


@monitor.route('/status/task')
@login_required
def task_status():
    return render_template('monitor/task_status.html')
