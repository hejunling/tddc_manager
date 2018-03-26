# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: forms.py
@time: 2018/3/20 19:07
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(),
                                                    Length(1, 64)])

    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(8, 16)])

    remember_me = BooleanField('Keep me login in')

    submit = SubmitField('Login')
