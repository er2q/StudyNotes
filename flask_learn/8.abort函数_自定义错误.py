# -*- coding:UTF-8 -*-

# author: cloudandsun
# contact: 1961879865@qq.com
# datetime:2022/3/14 23:26
# software: PyCharm

"""
文件说明：
    
"""
# raise 主动抛出异常
# abort 在网页中主动抛出异常
from flask import Flask, abort, request, make_response, render_template

app = Flask(__name__)


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index_abort.html')
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        if name == 'zhangsan' and password == '123':
            return 'login success'
        else:
            abort(404)
            return None


# 自定义错误处理方法
@app.errorhandler(404)
def handle_404_error(err):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
