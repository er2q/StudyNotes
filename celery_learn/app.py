# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/6/21 13:43
# software: PyCharm

"""
文件说明：
    
"""
# app.py
from task import add

if __name__ == '__main__':
    print("Start Task ...")
    result = add.delay(2, 8)
    print("result:", result)  # 存到redis之后，返回的id
    print("result_id:", result.id)  # 存到redis之后，返回的id
    print("result:", result.get())  # 方法返回值
    print("End Task ...")

