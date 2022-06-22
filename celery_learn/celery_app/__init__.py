# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 14:21
# software: PyCharm

"""
文件说明：
    
"""
# __init__.py 包初始化文件

from celery import Celery

app = Celery('demo')

app.config_from_object('celery_app.celeryconfig')  # 通过celery 实例加载配置文件
