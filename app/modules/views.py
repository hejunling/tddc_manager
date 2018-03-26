# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: views.py
@time: 2018/3/21 10:49
"""
from collections import defaultdict

from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required
from werkzeug.datastructures import FileStorage

from app import upload_set, db
from app.models import Modules
from app.modules.forms import FileSelectForm, FileEditForm
from app.modules.helper import get_modules_info, EventPusher, push_update_event
from . import modules


@modules.route('/list')
@login_required
def modules_list():
    modules_list = Modules.query.all()
    modules = defaultdict(list)
    for module in modules_list:
        modules[module.platform].append(module)
    return render_template('modules/modules_list.html', modules=modules)


@modules.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    file_select_form = FileSelectForm()
    if file_select_form.validate_on_submit():
        files = request.files.getlist('modules_file')
        platform = file_select_form.platform.data
        own = file_select_form.process_selector.data
        for _file in files:
            filename = upload_set.save(_file, name='{}/{}'.format(platform, _file.filename))
            file_url = upload_set.url(filename)
            modules, msg = get_modules_info(platform, filename, _file)
            if not modules:
                flash(msg)
                break
            modules.own = own
            modules.url = file_url
            m = Modules.query.filter_by(own=modules.own,
                                        platform=modules.platform,
                                        feature=modules.feature).first()
            if not m:
                db.session.add(modules)
                db.session.commit()
            else:
                m.update(modules)
        else:
            return redirect(url_for('modules.modules_list'))
    return render_template('modules/upload.html', file_select_form=file_select_form)


@modules.route('/<mid>/edit', methods=['POST', 'GET'])
@login_required
def edit_module(mid):
    form = FileEditForm()
    modules = Modules.query.get(int(mid))
    if not modules:
        return abort(404)
    filename = '{}/{}.py'.format(modules.platform, modules.package)
    if form.validate_on_submit():
        if request.form.get('cancel', None):
            return redirect(url_for('modules.modules_list'))
        content = form.code_editor.data
        with open('./PythonFiles/{}'.format(filename), 'w') as f:
            f.write(content.encode('utf-8'))
        upload_set.url(filename)
        flash(u'修改成功!')
        return redirect(url_for('modules.edit_module', mid=mid))
    if modules:
        with open('./PythonFiles/{}'.format(filename)) as f:
            content = f.read()
            form.code_editor.data = content.decode('utf-8').lstrip()
            return render_template('modules/editor.html',
                                   filename=filename,
                                   form=form)


@modules.route('/<mid>/push')
@login_required
def push_module(mid):
    modules = Modules.query.get(int(mid))
    if not modules:
        flash(u'找不到模块信息！')
        return abort(404)
    push_update_event(modules)
    flash(u'模块更新消息推送成功！')
    return redirect(url_for('modules.modules_list'))


@modules.route('/<mid>/delete')
@login_required
def delete_module(mid):
    modules = Modules.query.get(int(mid))
    if modules:
        db.session.delete(modules)
        db.session.commit()
    return redirect(url_for('modules.modules_list', modules=Modules.query.all()))
