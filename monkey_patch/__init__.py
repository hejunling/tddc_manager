# encoding: utf-8
"""
@version: ??
@author: chenyitao
@license: Apache Licence 
@software: PyCharm
@file: __init__.py.py
@time: 2018/3/22 09:33
"""

from flask_uploads_patch import patch as flask_uploads_patch


def patch_all():
    flask_uploads_patch()
