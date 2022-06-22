# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 13:48
# software: PyCharm

"""
文件说明：
    
"""
# check.py

from celery.result import AsyncResult
from task import app

async_result = AsyncResult(id="f83f7c19-f969-4121-8b6f-f591cd23d273", app=app)

if async_result.successful():
    result = async_result.get()
    print(result)
    # result.forget() # 将结果删除
elif async_result.failed():
    print('执行失败')
elif async_result.status == 'PENDING':
    print('任务等待中被执行')
elif async_result.status == 'RETRY':
    print('任务异常后正在重试')
elif async_result.status == 'STARTED':
    print('任务已经开始被执行')
