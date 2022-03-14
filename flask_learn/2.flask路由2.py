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


@app.route('/hello', methods=['GET', 'POST'])
def hello():
    return 'hello world'


@app.route('/hi', methods=['POST'])     # 失败
def hi():
    return 'hi'


if __name__ == '__main__':
    app.run()
