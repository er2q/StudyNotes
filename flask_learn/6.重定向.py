# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 23:04
# software: PyCharm

"""
文件说明：
    
"""
# 重定向 302

from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route('/index')
def index():
    # return redirect('https://www.baidu.com')
    return redirect(url_for('hello'))


@app.route('/')
def hello():
    return 'this is hello fun'


if __name__ == '__main__':
    app.run()
