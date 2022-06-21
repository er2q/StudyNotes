# -*- coding:UTF-8 -*-

# author: ErQ
# datetime:2022/3/21 16:47
# software: PyCharm

"""
文件说明：
    
"""
import time

def add(x, y):
    time.sleep(5)
    return x + y

if __name__ == '__main__':
    print('tast start....')
    result = add(2, 3)
    print('task end....')
    print(result)