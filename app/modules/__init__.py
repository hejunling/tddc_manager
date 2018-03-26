# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/21 10:48
"""

from flask import Blueprint

modules = Blueprint('modules', __name__)

from . import views
