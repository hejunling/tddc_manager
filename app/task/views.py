# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: views.py
@time: 2018/3/21 10:51
"""
import time
from flask import render_template, redirect, url_for
from flask_login import login_required

from app import db
from .models import MainTask
from app.task.forms import TaskForm
from . import task


@task.route('/list')
@login_required
def task_list():
    return render_template('task/task_list.html', task_list=MainTask.query.all())


@task.route('/<tid>/edit', methods=['GET', 'POST'])
@login_required
def edit_task(tid):
    main_task = MainTask.query.get(int(tid))
    form = TaskForm()
    if form.validate_on_submit():
        if not main_task:
            main_task = MainTask()
            db.session.add(main_task)
        main_task.timestamp = int(time.time())
        main_task.platform = form.platform.data
        main_task.feature = form.feature.data
        main_task.url = form.url.data
        main_task.method = form.method.data
        main_task.proxy = form.proxy.data
        main_task.space = int(form.space.data)
        main_task.headers = form.headers.data
        main_task.valid = form.valid.data
        db.session.commit()
        return redirect(url_for('task.task_list'))
    if int(tid) == -1:
        main_task = MainTask()
    form.update(main_task)
    return render_template('task/task_edit.html', form=form)


@task.route('/<tid>/delete', methods=['GET', 'POST'])
@login_required
def delete_task(tid):
    main_task = MainTask.query.get(int(tid))
    if main_task:
        db.session.delete(main_task)
        db.session.commit()
    return redirect(url_for('task.task_list'))
