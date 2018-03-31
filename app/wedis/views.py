# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: views.py
@time: 2018/3/30 10:59
"""

import time
from flask import render_template, jsonify, abort, request, flash
from flask_login import login_required
from tddc import StatusManager

from . import wedis


@wedis.route('/views')
@login_required
def views():
    return render_template('/wedis/views.html')


@wedis.route('/keys')
@login_required
def keys():
    print(time.time())
    keys = StatusManager().keys()
    print(time.time())

    def list_dict(d, l):
        if not len(l):
            return
        first = l[0]
        d[first] = {}
        l = l[1:]
        if len(l) > 0:
            list_dict(d[first], l)

    def merge_dict(d1, d2):
        keys1 = d1.keys()
        keys2 = d2.keys()
        for i in range(len(keys1) if len(keys1) < len(keys2) else len(keys2)):
            if keys1[i] != keys2[i]:
                if isinstance(keys1, list):
                    if keys2[i] in keys1:
                        merge_dict(d1[keys2[i]], d2[keys2[i]])
                        continue
                d1[keys2[i]] = d2[keys2[i]]
                return
            else:
                merge_dict(d1[keys1[i]], d2[keys1[i]])

    def make_nodes(data, nodes):
        for key, value in data.items():
            node = {'text': key}
            if value:
                node['nodes'] = []
                make_nodes(value, node['nodes'])
            nodes.append(node)

    all_fields = []
    for index, key in enumerate(keys):
        ks = key.split(':')
        tmp = {}
        list_dict(tmp, ks)
        all_fields.append(tmp)
    print(time.time())

    for i in range(len(all_fields) - 1):
        d1 = all_fields[0]
        d2 = all_fields[i + 1]
        merge_dict(d1, d2)
    print(time.time())

    nodes = []
    make_nodes(all_fields[0], nodes)
    print(time.time())
    return jsonify(nodes)


@wedis.route('/getKeyContent/<key>')
@login_required
def get_key_content(key):
    redis_methods = {'hash': StatusManager().hgetall,
                     'set': StatusManager().smembers,
                     'list': StatusManager().lrange,
                     'string': StatusManager().get}
    key_type = StatusManager().type(key)
    method = redis_methods.get(key_type)
    if not method:
        return abort(404)
    if key_type == 'list':
        data = method(key, 0, 100)
    elif key_type == 'string':
        data = {'value': method(key)}
    else:
        data = method(key)
    if isinstance(data, set):
        data = list(data)
    return jsonify({'result': data})


@wedis.route('/cmd')
@login_required
def cmd():
    command = request.args.get('command')
    if not cmd:
        flash(u'请输入命令')
        return jsonify({'error': u'请输入命令'})
    command = command.split(' ')
    if command[0] == 'clean':
        ret = StatusManager().clean(command[1])
        return jsonify({'result': ret})
    try:
        ret = StatusManager().execute_command(*command)
    except Exception as e:
        ret = e.message
    return jsonify({'result': ret})
