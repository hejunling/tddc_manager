# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/21 10:54
"""

from flask import Blueprint

monitor = Blueprint('monitor', __name__)

from . import views
