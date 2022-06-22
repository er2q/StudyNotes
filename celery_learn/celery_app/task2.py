# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 14:22
# software: PyCharm

"""
文件说明：
    
"""
# task2.py

from celery_app import app


@app.task
def multiply(x, y):
    print('Enter call function ...')
    return x * y
