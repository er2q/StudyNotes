# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/15 10:51
# software: PyCharm

"""
文件说明：
    
"""
# 模板 jinja2
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index')
def index():
    data = {
        'name': '张三',
        'age': 18,
        'mylist': [1, 2, 3, 4, 5, 6]
    }
    return render_template('index2.html', data=data)


if __name__ == '__main__':
    app.run()
