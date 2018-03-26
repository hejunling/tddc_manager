# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: forms.py
@time: 2018/3/21 12:46
"""

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import Length, DataRequired, URL, NumberRange


class TaskForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()], render_kw={'readonly': True})

    platform = StringField('Platform', validators=[DataRequired(), Length(1, 32)])

    feature = StringField('Feature', validators=[DataRequired(), Length(1, 32)])

    url = StringField('URL', validators=[DataRequired(), Length(1, 1024), URL()])

    method = StringField('Method', validators=[DataRequired(), Length(3, 8)])

    proxy = StringField('Proxy Type', validators=[Length(0, 8)])

    space = StringField('Space',
                        validators=[DataRequired()])

    headers = StringField('Headers', validators=[Length(0, 1024)])

    valid = BooleanField('Valid')

    timestamp = StringField('Timestamp', render_kw={'readonly': True})

    submit = SubmitField(u'提交')

    def update(self, task):
        self.id.data = str(task.id)
        self.url.data = task.url
        self.platform.data = task.platform
        self.feature.data = task.feature
        self.space.data = task.space
        self.headers.data = task.headers
        self.method.data = task.method
        self.proxy.data = task.proxy
        self.valid.data = bool(task.valid)
        self.timestamp.data = task.timestamp
