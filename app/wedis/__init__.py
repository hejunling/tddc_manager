# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/30 10:58
"""

from flask import Blueprint

wedis = Blueprint('wedis', __name__)

from . import views
