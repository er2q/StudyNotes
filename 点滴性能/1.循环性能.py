# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/19 18:08
# software: PyCharm

"""
文件说明：
    
"""
import time
import numpy as np


def for_1(arr):
    w, h = arr.shape
    sum = 0
    for i in range(w):
        for j in range(h):
            sum = + arr[i][j]
    return sum

def for_2(arr):
    w, h = arr.shape
    sum = 0
    for i in range(h):
        for j in range(w):
            sum = + arr[j][i]
    return sum

if __name__ == '__main__':
    aa = np.random.random(size=(20480, 4096))
    time1 = time.time()
    for_1(aa)
    time2 = time.time()
    for_2(aa)
    time3 = time.time()
    print(f'{time2-time1}:{time3-time2}')