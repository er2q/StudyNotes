# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 21:50
# software: PyCharm

"""
文件说明：
    
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
