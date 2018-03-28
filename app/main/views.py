# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: views.py
@time: 2018/3/20 17:55
"""
from flask import render_template, request, json, jsonify
from flask_login import login_required

from app.main.helper import SystemResourceMonitor
from . import main


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/sys_res_used', methods=['GET', 'POST'])
@login_required
def sys_res_used():
    last_24_hour = SystemResourceMonitor().last_24_hour_used()
    last_24_hour = [item.to_dict() for item in last_24_hour]
    data = json.dumps(last_24_hour)
    if request.args.get('callback'):
        return u'{}({})'.format(request.args.get('callback'), data)
    else:
        return jsonify(data)
