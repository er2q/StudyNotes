# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 21:14
# software: PyCharm

"""
文件说明：
    
"""
# 路由
from flask import Flask

app = Flask(__name__)


@app.route('/user/<id>')  # 用<> 正则匹配方式
def index(id):
    if id == '1':
        return 'python'
    if id == str(2):
        return 'django'
    if int(id) == 3:
        return 'flask'
    return 'hello world'


if __name__ == '__main__':
    app.run()
