# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: forms.py
@time: 2018/3/21 15:50
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, SubmitField, FileField, RadioField, TextAreaField
from wtforms.validators import Length, DataRequired, Optional

from app import upload_set


class FileSelectForm(FlaskForm):
    modules_file = FileField(validators=[FileAllowed(upload_set, 'Python File Only!')],
                             render_kw={'multiple': 'multiple',
                                        'style': ('position:absolute; '
                                                  'filter:alpha(opacity=0);'
                                                  'opacity:0;width:30px;'),
                                        'onchange': 'display()'})
    select_files = SubmitField(u'请选择文件',
                               render_kw={'onclick': "$('#modules_file').click();",
                                          'type': "button"})
    files = StringField(render_kw={'readonly': True,
                                   'style': 'no-repeat 60px center;'})
    process_selector = RadioField('Process',
                                  validators=[Optional()],
                                  choices=[('Crawler', 'Crawler'),
                                           ('Parser', 'Parser'),
                                           ('Proxy Checker', 'Proxy')],
                                  default=1)
    platform = StringField(validators=[DataRequired(), Length(1, 32)],
                           render_kw={'class': 'input-lg'})
    submit = SubmitField(u'上传')


class FileEditForm(FlaskForm):
    code_editor = TextAreaField(validators=[DataRequired()])
    commit = SubmitField(u'提交')
    cancel = SubmitField(u'取消/返回')
