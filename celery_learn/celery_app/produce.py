# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 14:23
# software: PyCharm

"""
文件说明：
    
"""
# produce.py

from celery_app.task1 import add 	# 在这里我只调用了task1

if __name__ == '__main__':
    print("Start Task ...")
    re = add.delay(7, 5)
    print(re.id)
    print(re.status)
    print(re.get())
    print("End Task ...")
