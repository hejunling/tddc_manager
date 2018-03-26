# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/20 17:55
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import forms
from . import views
