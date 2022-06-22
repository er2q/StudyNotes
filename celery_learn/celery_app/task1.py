# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 14:22
# software: PyCharm

"""
文件说明：
    
"""
# task1.py

from celery_app import app


# 加入装饰器变成异步的函数
@app.task
def add(x, y):
    print('Enter call function ...')
    return x + y

