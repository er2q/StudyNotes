# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 14:22
# software: PyCharm

"""
文件说明：
    
"""
# celeryconfig.py

from datetime import timedelta
from celery.schedules import crontab

# 参数配置文件celeryconfig.py

BROKER_URL = 'redis://localhost:6379/1'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
CELERY_TIMEZONE = "Asia/shanghai"  # 默认UTC
CELERY_RESULT_SERIALIZER = 'msgpack'

# 导入指定的任务模块
CELERY_IMPORTS = (
    'celery_app.task1',
    'celery_app.task2',
)

# 设置定时任务
CELERYBEAT_SCHEDULE = {
    # 每过10秒执行以下task1.add的定时任务
    'task1': {
        'task': 'celery_app.task1.add',
        'schedule': timedelta(seconds=10),
        'args': (2, 8)
    },
    # 等到22点18分执行task2的multiply
    'task2': {
        'task': 'celery_app.task2.multiply',
        'schedule': crontab(hour=14, minute=40),
        'args': (4, 5)
    }
}
