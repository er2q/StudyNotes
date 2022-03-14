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


# string 接受任何不包含斜杠的文本
# int 接受正整数
# float 接受正浮点数
# path 接受包含斜杠的文本
@app.route('/user/<int:id>')  # 用<> 正则匹配方式
def index(id):
    if id == 1:
        return 'python'
    if id == 2:
        return 'django'
    if id == 3:
        return 'flask'
    return 'hello world'


if __name__ == '__main__':
    app.run()
